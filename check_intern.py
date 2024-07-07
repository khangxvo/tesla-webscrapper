import json
import sys


def main():

    file_path = 'interns_w_descriptions.json'

    with open(file_path, 'r') as file:
        data = json.load(file)

    magic_num = 153  # Initial data length

    for job in data:
        if (job['type'] != 'intern'):
            print(json.dumps(job, indent=4))
            sys.exit(1)

    print(len(data) == 153)
    print('All jobs are internships')


if __name__ == "__main__":
    main()
