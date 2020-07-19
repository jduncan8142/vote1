import pandas as pd
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("--results", required=False, default="poll-results-export.csv",
                help="Specify the path to the CSV input file for Poll Results.")
ap.add_argument("--results_header", required=False, default=36,
                help="Integer for number of the row for header row of Poll Results file. Zero based index.")
ap.add_argument("--results_fields", required=False, help="Python list of field names in order for the voter data file",
                default=["Code", "Name", "Votes"])
ap.add_argument("--votes", required=False, default="poll-votes.csv", help="Output file path and name.")
ap.add_argument("--votes_header", required=False, default="36", help="Header value for column names")
ap.add_argument("--votes_fields", required=False,
                default=["ID", "Voter", "Email", "Poll", "Choice", "Date", "LoginSource", "Browser", "Mobile", "Code"])
args = vars(ap.parse_args())

df_voter_codes = pd.read_csv(args["results"], sep=",", header=args["results_header"], names=args["results_fields"])

print(f"Total Voter Codes: {len(df_voter_codes)}")
bad_voters = []
for index, row in df_voter_codes.iterrows():
    if row[args["results_fields"][2]] > 1:
        bad_voters.append({row["Code"]: row["Name"]})
print(f"Voters with more than 1 vote recorded: \n\tTotal: {len(bad_voters)} \n\tNames: ")
for x in bad_voters:
    [print(f"\t\t{i}") for i in x.values()]
df_voter_codes.drop(df_voter_codes[df_voter_codes[args["results_fields"][2]] > 1].index, inplace=True)
df_voter_codes.drop(df_voter_codes[df_voter_codes[args["results_fields"][2]] < 1].index, inplace=True)
print(f"Total voters responding (valid voters): {len(df_voter_codes[args['results_fields'][0]].to_list())}")

df_poll_votes = pd.read_csv(args["votes"], sep=",", header=int(args["votes_header"]), names=args["votes_fields"])

valid_records = []
invalid_records = []
for index, row in df_poll_votes.iterrows():
    if any(row["Code"] in k for k in bad_voters):
        invalid_records.append(row.to_dict())
    else:
        valid_records.append(row.to_dict())

print(f"Invalid records: ")
print(f"Total invalid records: {len(invalid_records)}")
# [print(x) for x in invalid_records]
print(f"Total valid records: {len(valid_records)}")


