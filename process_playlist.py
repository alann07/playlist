import argparse
import json
import logging
import sys
from playlist_service import PlaylistService

logger = logging.getLogger(__name__)


def parse_args():
    input_f = '<input-file>'
    change_f = '<changes-file>'
    output_f = '<output-file>'
    parser = argparse.ArgumentParser()
    parser.add_argument(input_f, help="playlist input file")
    parser.add_argument(change_f, help="playlist changes file")
    parser.add_argument(output_f, help="playlist output-file")

    args = parser.parse_args()
    args_dict = vars(args)

    f = None
    try:
        f = open(args_dict[input_f], "r")
        input_json = json.load(f)
    except ValueError as e:
        logger.error('Input JSON error: {0}'.format(e))
        sys.exit(-1)
    except Exception as e:
        logger.error(format(e))
        sys.exit(-1)
    else:
        if f:
            print('closing the file')
            f.close()

    f2 = None
    try:
        f2 = open(args_dict[change_f], "r")
        changes_json = json.load(f2)
    except ValueError as e:
        logger.error('Changes JSON error: {0}'.format(e))
        sys.exit(-1)
    except Exception as e:
        logger.error(format(e))
        sys.exit(-1)
    else:
        if f2:
            f2.close()

    f3 = None
    try:
        f3 = open(args_dict[output_f], "w")
    except Exception as e:
        logger.error(format(e))
        sys.exit(-1)

    return input_json, changes_json, f3


def main():
    logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler()],
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    input_json, changes_json, output_file = parse_args()
    playlist_service = PlaylistService()
    error_list = playlist_service.apply_changes(input_json, changes_json, output_file)
    if len(error_list) == 0:
        logger.info("Playlist Processing Successful")
    else:
        logger.info("Playlist processing has errors:")
        for error in error_list:
            for k, v in error.items():
                logger.info(k + ": " + v)


if __name__ == '__main__':
    main()