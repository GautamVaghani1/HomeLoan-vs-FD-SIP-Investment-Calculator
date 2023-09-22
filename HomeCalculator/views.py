from django.shortcuts import render,redirect

def home(request):

    global data
    data = {}
    
    if request.method == "POST":
        try:
            name = request.POST.get('name')
            value = int(request.POST.get('value'))
            downpayment = int(request.POST.get('downpayment'))   
            interest = float(request.POST.get('interest'))
            years = int(request.POST.get('years'))
            
            amount = value - downpayment
            monthly_rate = (interest / 12) / 100
            loan_month = years * 12
            emi = (amount * monthly_rate * (1 + monthly_rate) ** loan_month) / ((1 + monthly_rate) ** loan_month - 1)
            total_payment = emi * 12 * years
            total_interest = total_payment - amount

            data = {
                'name': name,
                'value':value,
                'amount': amount,
                'interest': interest,
                'years': years,
                'monthly_rate': monthly_rate,
                'emi': round(emi),
                'total_payment': round(total_payment),
                'total_interest': round(total_interest),
                'downpayment':downpayment,

            }     

            request.session['home_data'] = data
        except ValueError:
           pass

    return render(request, 'home.html', data)

def benifit(request):
    data = request.session.get('home_data', {})
    

    rate = float( 6 / 100)
    rent = data.get('emi') * 35 / 100

    monthly_investment = data.get('emi') - rent
    n = 12
    r = 12 / 100 /12


    fd_return = data.get('downpayment') * (1+ rate / 1) ** (1 * data.get('years'))
    sip_return = monthly_investment * ((1 + r) ** (n * data.get('years')) - 1) / r

    final_amount = fd_return + sip_return


    return render(request,'benifit.html',{'data':data, 'fd_return':round(fd_return), 'rent':round(rent) , 'sip_return':round(sip_return) , 'final_amount' : round(final_amount)})