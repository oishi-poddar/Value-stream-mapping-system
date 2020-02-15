import pymongo
import datetime
from datetime import timedelta
import config


# Input Argument- 0:script name, 1:status of PR to gain the data, 2:number of days
def p2_git(status, n_days):
    if status is None:
        status = 'closed'
    if n_days is None:
        n_days = 30
    #my_client = pymongo.MongoClient(config.server)
    my_db = config.client[config.mongodb['dbname']]
    my_col = my_db['git_data_' + status]
    total_count_pr = my_col.count_documents({})
    n_days = int(n_days)
    day = datetime.datetime.now() - timedelta(days=n_days)
    e_data = my_col.find({"closed_at": {"$gt": day}})
    number_of_pr = 0
    count_jira_id = 0
    count_label_ContinuousLocalization = 0
    total_duration_to_merge = 0
    total_duration_to_close = 0
    total_review_comment_count = 0
    pr_without_review_comment = 0
    for d in e_data:
        if d['jira_id']:
            count_jira_id += 1
        if d['label_ContinuousLocalization']:
            count_label_ContinuousLocalization += 1
        if d['review_comment_count'] == 0:
            pr_without_review_comment += 1
        total_review_comment_count += d['review_comment_count']
        if d['duration_to_merge'] is not None:
            total_duration_to_merge += float(d['duration_to_merge'])
        if d['duration_to_close'] is not None:
            total_duration_to_close += float(d['duration_to_close'])
        number_of_pr += 1

    count_without_jira_id = number_of_pr - count_jira_id - count_label_ContinuousLocalization
    total_duration_to_merge = float("{0:.3f}".format(total_duration_to_merge))
    total_duration_to_close = float("{0:.3f}".format(total_duration_to_close))
    avg_review_comment_count = float("{0:.3f}".format(total_review_comment_count / number_of_pr))
    avg_duration_to_close = float("{0:.3f}".format(total_duration_to_close / number_of_pr))
    avg_duration_to_merge = float("{0:.3f}".format(total_duration_to_merge / number_of_pr))
    percentage_having_jira_id = float("{0:.2f}".format((count_jira_id / number_of_pr) * 100))
    percentage_label_ContinuousLocalization = float(
        "{0:.2f}".format((count_label_ContinuousLocalization / number_of_pr) * 100))
    percentage_without_having_jira_id = 100 - percentage_having_jira_id - percentage_label_ContinuousLocalization
    json_data = {
        # '_id': status,  # As the _id given my mongoDB is not JSON serializable
        'timestamp:': datetime.datetime.now(),
        'status': status,
        'number_of_days': n_days,
        'total_count_pr': total_count_pr,
        'number_of_pr': number_of_pr,
        'count_jiraId_and_ContinuousLocalization': count_label_ContinuousLocalization + count_jira_id,
        'count_jira_id': count_jira_id,
        'count_label_ContinuousLocalization': count_label_ContinuousLocalization,
        'count_without_jira_id': count_without_jira_id,
        'percentage_jiraId_and_ContinuousLocalization': percentage_having_jira_id + percentage_label_ContinuousLocalization,
        'percentage_without_having_jira_id': percentage_without_having_jira_id,
        'total_duration_to_merge': total_duration_to_merge,
        'avg_duration_to_merge': avg_duration_to_merge,
        'total_duration_to_close': total_duration_to_close,
        'avg_duration_to_close': avg_duration_to_close,
        'total_review_comment_count': total_review_comment_count,
        'avg_review_comment_count': avg_review_comment_count,
        'pr_without_review_comment': pr_without_review_comment,
    }
    # my_db['extract'].delete_many({})
    # my_db['extract'].insert_one(json_data)
    # print(json_data)
    return json_data

p2_git('closed',30)