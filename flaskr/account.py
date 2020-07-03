from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('account', __name__)

@bp.route('/')
def index():
    db = get_db()
    transactions = db.execute(
        'SELECT a.id, a.acct_name, a.balance, type, amount, occurred'
        ' FROM transactions t JOIN account a ON t.account_id = a.id'
        ' ORDER BY occurred DESC'
    ).fetchall()
    balance = db.execute(
        'SELECT balance'
        ' FROM account'
        ' WHERE id = ?',
        (g.user['id'],)
    ).fetchone()
    return render_template('account/index.html', transactions=transactions, balance=balance[0])


@bp.route('/deposit', methods=('GET', 'POST'))
@login_required
def deposit():
    if request.method == 'POST':
        amount = request.form['amount']
        error = None

        if not amount:
            error = 'Amount is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO transactions (amount, type, account_id)'
                ' VALUES (?, ?, ?) ',
                (amount, "deposit", g.user['id'])
            )
            balance = get_db().execute(
                    'SELECT balance'
                    ' FROM account'
                    ' WHERE id = ?',
                    (g.user['id'],)
                ).fetchone()
            db.execute(
                'UPDATE account SET balance = ?'
                ' WHERE id = ?',
                (float(amount)+float(balance[0]), g.user['id'])
            )
            db.commit()
            return redirect(url_for('account.index'))
    return render_template('account/deposit.html')

@bp.route('/withdraw', methods=('GET', 'POST'))
@login_required
def withdrawal():
    if request.method == 'POST':
        amount = request.form['amount']
        error = None

        if not amount:
            error = 'Amount is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO transactions (amount, type, account_id)'
                ' VALUES (?, ?, ?) ',
                (amount, "withdrawal", g.user['id'])
            )
            balance = get_db().execute(
                    'SELECT balance'
                    ' FROM account'
                    ' WHERE id = ?',
                    (g.user['id'],)
                ).fetchone()
            db.execute(
                'UPDATE account SET balance = ?'
                ' WHERE id = ?',
                (float(balance[0]) - float(amount), g.user['id'])
            )
            db.commit()
            return redirect(url_for('account.index'))
    return render_template('account/withdraw.html')


