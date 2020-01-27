#!/usr/bin/env python

import os
import argparse

from tests.case_0_ import case_0_
from tests.case_1_ import case_1_
from tests.case_2_ import case_2_
from tests.case_3_ import case_3_
from tests.case_4_ import case_4_
from tests.case_5_ import case_5_
from tests.case_6_ import case_6_
from tests.case_7_ import case_7_
from tests.case_8_ import case_8_


def example(IDnumber=0):

#--------------- delegate to the individual example cases...

    src_path = os.path.join(
        os.path.abspath(
            os.path.dirname(__file__)), "files")

    dst_path = os.path.join(
        os.path.abspath(
            os.path.dirname(__file__)), "cache")

    if   (IDnumber == +0):
        case_0_(src_path, dst_path)

    elif (IDnumber == +1):
        case_1_(src_path, dst_path)

    elif (IDnumber == +2):
        case_2_(src_path, dst_path)

    elif (IDnumber == +3):
        case_3_(src_path, dst_path)

    elif (IDnumber == +4):
        case_4_(src_path, dst_path)

    elif (IDnumber == +5):
        case_5_(src_path, dst_path)

    elif (IDnumber == +6):
        case_6_(src_path, dst_path)

    elif (IDnumber == +7):
        case_7_(src_path, dst_path)

    elif (IDnumber == +8):
        case_8_(src_path, dst_path)

    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument("--IDnumber", dest="IDnumber", type=int,
                        required=True, help="Run example with ID = (0-9).")

    args = parser.parse_args()

    example(IDnumber=args.IDnumber)
