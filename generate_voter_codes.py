import pandas as pd
import string
import random
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("--input", required=False, default="data.xlsx",
                help="Specify the path to the XLSX input file of voter information.")
ap.add_argument("--sheet", required=False, default="Total")
ap.add_argument("--fields", required=False, help="Python list of field names in order for the voter data file",
                default=["LastName", "FirstName", "Age", "Primary", "Street", "City", "State", "Zip", "MobilePhone",
                         "HomePhone", "LastAttendedDate", "Membership"])
ap.add_argument("--header", required=False, default=4, help="Integer for number of the row for header row of voter "
                                                            "data file. Zero based index.")
ap.add_argument("--membership_col", required=False, default=11, help="Number of membership column,")
ap.add_argument("--membership_label", required=False, default="Member", help="Membership column header name.")
ap.add_argument("--output", required=False, default="voter_codes.txt", help="Output file path and name.")
args = vars(ap.parse_args())

df = pd.read_excel(
    args["input"],
    sheet_name=args["sheet"],
    names=args["fields"],
    header=int(args["header"]),
    usecols=args["fields"],
)
df.drop(df[df[args["fields"][int(args["membership_col"])]] != args["membership_label"]].index, inplace=True)
member_list = []
code_list = []
for index, row in df.iterrows():
    res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    code_list.append(res)
    member_list.append(f"{res},{row[args['fields'][1]]} {row[args['fields'][0]]},{row[args['fields'][8]]}\n")
code_list = set(code_list)
print(f"Total Members: {len(member_list)}")
print(f"Total Voter Codes: {len(code_list)}")
with open(args["output"], "w") as fn:
    fn.writelines(member_list)
print("Done!")
