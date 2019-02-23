from __future__ import division
import json
import stackapi
from itertools import chain
from json2html import json2html



class stackstats:
    """
    The object represent the core of Encode Python Assignment
       - Retrieve the StackOverflow answer data for a given date/time range from the StackExchange API
       - Retrieve the comment data for a given set of answers
    For a given date/time range calculate:
       - the total number of accepted answers.
       - the average score for all the accepted answers.
       - the average answer count per question.
       - the comment count for each of the 10 answers with the highest score.
       - Collect and return the calculated statistics in HTML or JSON format.

        :Input:
                :param options:   (Dictionary) **(Required)** It must have at least --output format.

    """

    def __init__(self, options):

        if options.has_key('fromdate'):
            self._fromdate = options['fromdate']
        if options.has_key('todate'):
            self._todate = options['todate']
        if options.has_key('output'):
            self._output_format = options['output']

        self.SITE = stackapi.stacks('stackoverflow')

    def get_answer_data(self):
        """
        This method return the answer data that it has received from Stackoverflow API
        It use the options that has the constructor of the object.

        :Output:
            :answer_data:  (list) It returnes a list with the answered_data that it has received
                            from the API
        """
        params, url = self.SITE.stacks_answer(
            fromdate=self._fromdate, todate=self._todate, sort='votes')
        answer_data = self.SITE.fetch_data(url, params)
        return answer_data

    def get_comment_on_answer_data(self, ids):
        """
        This method return the comment data from specific answers that it has received from Stackoverflow API
        It use the options that has the constructor of the object.
        
        :Input:
                :ids: (list)**(Required)** A list with ids of the answers that you want to get comments

        :Output:
            :comment_data:  (list) It returnes a list with the comment_data that it has received
                            from the API
        """
        # The API accept an id list with 100 values maximum
        # If the len(ids)>100 it split ids list to N parts
        if len(ids) > 100:
            n = 100
            comment_data = []
            ids_parts = [ids[i * n:(i + 1) * n]
                         for i in range((len(ids) + n - 1) // n)]
            for id in ids_parts:
                params, url = self.SITE.stacks_comments_on_answers(
                    fromdate=self._fromdate, todate=self._todate, ids=id)
                temp = self.SITE.fetch_data(url, params)
                comment_data.extend(temp)
        else:
            params, url = self.SITE.stacks_comments_on_answers(
                fromdate=self._fromdate, todate=self._todate, ids=id)
            comment_data = (self.SITE.fetch_data(url, params))

        return comment_data

    def calc_stats(self, answer_data, comment_data):
        """
        This method get as input the answer_data,comment_data and 
        print the stats  which was requested that python assigment in 
        
        :Input:
                :answer_data:   (list)**(Required)** A list with answers_data that it has received from the API.

                :comment_data:  (list)**(Required)** A list with comment_data that it has received from the API.
        """
        # the total number of accepted answers.
        total_accepted_answers = len([item for item in answer_data if item['is_accepted'] == True])

        # the average score for all the accepted answers.
        score = ([item['score'] for item in answer_data if item['is_accepted'] == True])
        accepted_answers_average_score = float(sum(score)/len(score))

        # the average answer count per question
        questions = ([item['question_id'] for item in answer_data])
        questions = list(set(questions))
        average_answers_per_question = float(len(answer_data)/len(questions))

        # the comment count for each of the 10 answers with the highest score.
        # The answers with the highest score are the first 10 answers because
        # I used sortes = 'votes'
        first10Answers = [answer_data[i]['answer_id'] for i in range(10)]
        # this list contains all post_ids for comments
        comments = [item['post_id'] for item in comment_data]
        commentCount = {}
        # Count how many times 'answer_id' = 'post_id'
        for answer in first10Answers:
            count = comments.count(answer)
            commentCount[answer] = count

        data = {}
        data["total_accepted_answers"] = total_accepted_answers
        data["accepted_answers_average_score"] = accepted_answers_average_score
        data["average_answers_per_question"] = average_answers_per_question
        data["top_ten_answers_comment_count"] = commentCount
        json_data = json.dumps(data)

        if self._output_format == 'json':

            print(json.dumps(data, indent=4))
            with open("stats.json", "w") as file:
                file.write(json_data)
        elif self._output_format == 'html':
            html_data = json2html.convert(json=json_data)
            with open("stats.html", "w") as file:
                file.write(html_data)
