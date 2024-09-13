# app.py
from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

# Simple interest calculation function
def calculate_simple_interest(principal, rate, time):
    total_interest = (principal * rate * time) / 100
    total_payment = principal + total_interest
    monthly_interest = total_interest / (time * 12)  # Monthly interest for the duration
    monthly_principal = principal / (time * 12)     # Monthly principal amount
    return {
        'total_interest': total_interest,
        'total_payment': total_payment,
        'monthly_interest': monthly_interest,
        'monthly_principal': monthly_principal
    }

# Calculate remaining months/years and outstanding balance
def calculate_remaining_outstanding(principal, total_payment, last_payment_date, end_date):
    today = datetime.today()
    
    # Calculate months/years between today and the end date
    remaining_months = (end_date.year - today.year) * 12 + (end_date.month - today.month)
    remaining_years = remaining_months // 12
    remaining_months = remaining_months % 12

    # Assume user pays monthly; calculate outstanding amount based on months since last payment
    months_since_last_payment = (today.year - last_payment_date.year) * 12 + (today.month - last_payment_date.month)
    outstanding = total_payment - (months_since_last_payment * (total_payment / (end_date - last_payment_date).days * 30))

    return {
        'remaining_years': remaining_years,
        'remaining_months': remaining_months,
        'outstanding_amount': outstanding
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    show_form = True
    if request.method == 'POST':
        # Extract form values
        principal = request.form.get('principal')
        rate = request.form.get('rate')
        time = request.form.get('time')
        start_date = request.form.get('start_date')
        last_payment_date = request.form.get('last_payment_date')
        end_date = request.form.get('end_date')

        if principal and rate and time and start_date:
            # Perform simple interest calculation
            principal = float(principal)
            rate = float(rate)
            time = float(time)
            start_date = datetime.strptime(start_date, '%Y-%m-%d')

            # Calculate interest info
            interest_info = calculate_simple_interest(principal, rate, time)
            
            if last_payment_date and end_date:
                # Convert additional dates
                last_payment_date = datetime.strptime(last_payment_date, '%Y-%m-%d')
                end_date = datetime.strptime(end_date, '%Y-%m-%d')

                # Calculate remaining outstanding balance
                outstanding_info = calculate_remaining_outstanding(
                    principal, interest_info['total_payment'], last_payment_date, end_date)

                # Include additional details in result
                result = {
                    'principal': principal,
                    'rate': rate,
                    'time': time,
                    'total_interest': interest_info['total_interest'],
                    'total_payment': interest_info['total_payment'],
                    'monthly_interest': interest_info['monthly_interest'],
                    'monthly_principal': interest_info['monthly_principal'],
                    'remaining_years': outstanding_info['remaining_years'],
                    'remaining_months': outstanding_info['remaining_months'],
                    'outstanding_amount': outstanding_info['outstanding_amount']
                }
            else:
                # Show only initial calculation results
                result = {
                    'principal': principal,
                    'rate': rate,
                    'time': time,
                    'total_interest': interest_info['total_interest'],
                    'total_payment': interest_info['total_payment'],
                    'monthly_interest': interest_info['monthly_interest'],
                    'monthly_principal': interest_info['monthly_principal']
                }

            # Disable form fields and show results
            show_form = False

    return render_template('index.html', result=result, show_form=show_form)

if __name__ == '__main__':
    app.run(debug=True)
