import argparse

from . import PodcastsFromMacOS



def prepare_args():
    parser = argparse.ArgumentParser(
        prog='macOS_podcasts',
        description='Export macOS Podcasts to OPML'
    )

    parser.add_argument(
        '--db',
        dest='podcasts_db',
        required=False,
        default=PodcastsFromMacOS.podcasts_db,
        help=f'Path to Podcasts app database. Default is «{PodcastsFromMacOS.podcasts_db}».'
    )

    parser.add_argument(
        '-g', '--group',
        dest='group',
        required=False,
        default='apple_category',
        help='Group podcasts in the outline by station, author or apple_category. Defaults to apple_category.'
    )

    parser.add_argument(
        '--trees',
        dest='trees',
        action=argparse.BooleanOptionalAction,
        default=False,
        help='Export to one hierarchical file (default), or to one file per group.'
    )
    
    parser.add_argument(
        '--target',
        dest='target',
        required=False,
        default=None,
        help='Target folder for exported OPML files. Default is current folder.'
    )

    parser.add_argument(
        '--prefix',
        dest='prefix',
        required=False,
        default=None,
        help=f'File name prefix for each OPML file. Default is «{PodcastsFromMacOS.file_prefix}»'
    )

    return parser.parse_args()
    

    
    
def main():
    # Read environment and command line parameters
    args=prepare_args()
    
    p=PodcastsFromMacOS(args.podcasts_db)
    
    p.export(
        p.opml(
            group=args.group,
            trees=args.trees
        ),
        target_folder=args.target,
        file_prefix=args.prefix
    )



if __name__ == "__main__":
    main()