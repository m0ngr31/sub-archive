from app import app, db
from app.models import Submissions, Comments, get_count
from flask import render_template, request, abort
from sqlalchemy import desc


@app.route('/', methods=['GET'])
def home():
  """
  Homepage Route: Will show what subreddits are available in the configured database
  """

  subreddits = []

  # Loop through available subreddits
  for value in db.session.query(Submissions.subreddit).distinct():
    subreddit = {
      'name': value.subreddit,
      'comments': 0,
      'submissions': 0,
    }

    # Figure out how many submissions and comments each subreddit has
    comments_q = db.session.query(Comments).filter_by(subreddit=value.subreddit)
    submissions_q = db.session.query(Submissions).filter_by(subreddit=value.subreddit)

    subreddit['comments'] = get_count(comments_q)
    subreddit['submissions'] = get_count(submissions_q)

    subreddits.append(subreddit)

  return render_template('home.html', title="The Archive", description="The Archive", subreddits=subreddits)


@app.route('/r/<subreddit_name>', methods=['GET'])
def subreddit_home(subreddit_name):
  """
  Subreddit Route: This will show a list of the submissions available for a subreddit

  Args
  -----
  start : int, optional - This is the offset number for pagination
  sort : str, optional - Should be "top" or "new"
  """

  start_arg = int(request.args.get('start', 0) or 0)
  sort_arg = request.args.get('sort', 'NEW')

  if sort_arg.upper() not in ['TOP', 'NEW']:
    sort_arg = 'NEW'

  if sort_arg.upper() == 'NEW':
    sort = Submissions.created
  else:
    sort = Submissions.score

  submissions = Submissions.query.filter_by(subreddit=subreddit_name).order_by(desc(sort)).offset(start_arg * 50).limit(50).all()

  if len(submissions) > 0:
    # Get the total count of submissions to check for pagination stuff
    submissions_q = db.session.query(Submissions).filter_by(subreddit=subreddit_name)
    total_submissions = get_count(submissions_q)

    page_info = {
      "has_more": (total_submissions / 50) > (start_arg + 1),
      "has_prev": start_arg > 0,
      "next_page": start_arg + 1,
      "prev_page": (start_arg - 1) if (start_arg > 1) else 0,
      "sort": sort_arg
    }

    return render_template('subreddit_home.html', title=subreddit_name, page_info=page_info, description=subreddit_name, submissions=submissions, subreddit=subreddit_name)
  else:
    # Make 404 page
    abort(404)


@app.route('/r/<subreddit_name>/<submission_id>', methods=['GET'])
def submission(subreddit_name, submission_id):
  """
  Submission Comments Route: Will show the comments for a submission
  """

  # Make sure submission id is valid
  submission = Submissions.query.filter_by(subreddit=subreddit_name, idstr=submission_id).first_or_404()
  comments = []

  all_comments = Comments.query.filter_by(subreddit=subreddit_name, submission=submission_id).order_by(desc(Comments.score)).all()

  # Serialize all the comments
  for comment in all_comments:
    cleaned_comment = comment.serialize
    cleaned_comment['children'] = []
    comments.append(cleaned_comment)

  # Insert children comments into parent comment lists
  for comment in comments:
    if comment.get('parent') != submission_id:
      parent_comment_index = next((index for (index, c) in enumerate(comments) if c.get('idstr') == comment.get('parent')), None)

      if parent_comment_index > -1:
        comments[parent_comment_index]['children'].append(comment)

  # Only have parent comments at the top level
  comments = [c for c in comments if c.get('parent') == submission_id]

  return render_template('submission.html', subreddit=subreddit_name, title=submission.title, description=submission.title, comments=comments, submission=submission)


@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html', title="Uh-oh :'(", description="404 Not Found"), 404
