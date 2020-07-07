from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('predict', __name__)

@bp.route('/predict', methods=('GET', 'POST'))
@login_required
def bet():
    if request.method == 'POST':
        bet = request.form['bet']
        odds = request.form['odds']
        error = None

        if not bet:
            error = 'A bet must be placed.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            # TODO: add bet and odds to database for tracking how well predictor performs
            balance = get_db().execute(
                    'SELECT balance'
                    ' FROM account'
                    ' WHERE id = ?',
                    (g.user['id'],)
                ).fetchone()
            db.execute(
                'UPDATE account SET balance = ?'
                ' WHERE id = ?',
                (float(balance[0]) - float(bet), g.user['id'])
            )
            db.commit()
            return redirect(url_for('predict.postfight'))
    return render_template('predict/index.html')


@bp.route('/postfight', methods=('GET', 'POST'))
@login_required
def postfight():
    if request.method == 'POST':
        winner = request.form['odds']
        error = None

        if not bet:
            error = 'A winner must be entered.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            # TODO: if the winner is the same as predicted, deposit winnings + original bet
            # TODO: if the winner is not the same as predicted, do nothing (money already removed)
            db.commit()
            return redirect(url_for('predict.postfight'))
    return render_template('predict/postfight.html')
