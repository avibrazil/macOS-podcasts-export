import sqlite3
import glob
import pathlib
import xml.etree.ElementTree
import pandas



class PodcastsFromMacOS:
    file_prefix='macOS-Podcasts'
    
    podcasts_db='~/Library/Group Containers/*.groups.com.apple.podcasts/Documents/MTLibrary.sqlite'

    query="""
        WITH pod_playlist AS (
            SELECT pp.ZPODCAST,playlists.ZTITLE
            FROM ZMTPODCASTPLAYLISTSETTINGS pp
            LEFT JOIN ZMTPLAYLIST AS playlists
                ON playlists.Z_PK = pp.ZPLAYLIST
            WHERE playlists.Z_PK > 2
        )
        
        SELECT
            pod_playlist.ZTITLE         as station,
            podcast.Z_PK                as podcast_id,
            podcast.ZSORTORDER          as sort_order,
            datetime(podcast.ZADDEDDATE+strftime('%s','2001-01-01'),'unixepoch') as date_added,
            podcast.ZAUTHOR             as author,
            podcast.ZCATEGORY           as apple_category,
            podcast.ZTITLE              as name,
            podcast.ZWEBPAGEURL         as web,
            podcast.ZFEEDURL            as feed,
            podcast.ZIMAGEURL           as image,
            podcast.ZITEMDESCRIPTION    as description

        FROM ZMTPODCAST AS podcast

        LEFT OUTER JOIN pod_playlist
            ON pod_playlist.ZPODCAST = podcast.Z_PK

        ORDER BY station
    """

    
    def __init__(self,podcasts_db=None):
        if podcasts_db:
            self.podcasts_db=podcasts_db


    
    @property
    def podcasts(self):
        self._podcasts=(
            pandas.read_sql_query(
                self.query,
                con=sqlite3.connect(
                    [
                        pathlib.Path(p)
                        for p in glob.glob(
                            str(pathlib.Path(self.podcasts_db).expanduser()))
                    ][0]
                )
            )
            .assign(
                station         = lambda table: table.station.fillna('«None»'),
                author          = lambda table: table.author.fillna('«None»'),
                apple_category  = lambda table: table.apple_category.fillna('«None»')
            )
            .assign(
                station         = lambda table: pandas.Categorical(table.station),
                author          = lambda table: pandas.Categorical(table.author),
                apple_category  = lambda table: pandas.Categorical(table.apple_category),
                date_added      = lambda table: pandas.to_datetime(table.date_added)
            )
        )
        
        return self._podcasts



    def opml(self,group='apple_category',trees=False) -> dict:
        """
        Export the list of podcasts and their groupings to one or multiple OPML
        trees.
        """
        
        # First convert podcasts into OPML ‘<outline>’ elements
        p=self.podcasts.assign(
            element=lambda table: table.apply(
                lambda row: xml.etree.ElementTree.Element(
                    'outline',
                    dict(
                        type    =   "rss",
                        text    =   row['name']   if row['name']   else '',
                        xmlUrl  =   row['feed']   if row['feed']   else '',
                        htmlUrl =   row['web']    if row['web']    else '',
                        imgUrl  =   row['image']  if row['image']  else '',
                    )
                ),
                axis=1
            ),
            element_text=lambda table: table.apply(
                lambda row: xml.etree.ElementTree.tostring(row['element']),
                axis=1
            )
        )        
        
        
        # Now decide how to group them

        opmls={}
        groups=[]
        
        if group:
            groups+=p[group].unique().to_list()
                    
        opml_skel='<opml version="1.0"><head><title/></head><body/></opml>'
            
        if trees:
            for g in groups:
                opmls[g]=xml.etree.ElementTree.fromstring(opml_skel)
                opmls[g].find('head').find('title').text = f'macOS Podcasts: {group} is {g}'
                
                # Insert all podcasts
                opmls[g].find('body').extend(p.query(f"{group} == @g").element.to_list())
        else:
            tree='global'
            opmls[tree]=xml.etree.ElementTree.fromstring(opml_skel)
            opmls[tree].find('head').find('title').text = f'macOS Podcasts'
            
            for g in groups:
                e = xml.etree.ElementTree.Element(
                    'outline',
                    dict(
                        type    =   "group",
                        text    =   f'macOS Podcasts: {group} is {g}'
                    )
                )
                opmls[tree].find('body').append(e)                
                e.extend(p.query(f"{group} == @g").element.to_list())

        return opmls



    def export(self, opmls: dict, target_folder=None, file_prefix=None):
        for k in opmls.keys():
            xml.etree.ElementTree.indent(opmls[k], space="\t", level=0)
            doc=xml.etree.ElementTree.ElementTree(opmls[k])
            file_prefix=file_prefix if file_prefix else self.file_prefix
            file_path=pathlib.Path(f'{file_prefix}-{k}.opml')
            
            if target_folder:
                file_path=pathlib.Path(target_folder).expanduser() / file_path
            
            doc.write(file_path, encoding="utf-8", xml_declaration=True)