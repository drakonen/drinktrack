from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.db.models import Sum, Case, When

from .models import Consumption, Drink, User


def front_list(request):

    # madness
    users = User.objects.values('id', 'name').annotate(
        num_drinks=Sum(
            Case(
                When(
                    consumption__drink=1, then='consumption__count')
            )
        )
    ).order_by("id")

    for u in users:
        if u['num_drinks']:
            u['num_drinks'] = u['num_drinks'] * -1

    context = {
        'users': users
    }

    return render(request, 'front_list.html', context)


def user_detail(request, user_id):
    user_id = get_object_or_404(User, pk=user_id)

    drinks = Consumption.objects.filter(user=user_id).values('drink__name', 'drink__crate_size', 'drink').annotate(drink_sum=Sum('count'))

    available_drinks = Drink.objects.all()

    # convert to regular dict
    ndrinks = []
    for d in drinks:
        ndrinks.append({
            'drink__name': d['drink__name'],
            'drink_sum': d['drink_sum'] * -1,
            'drink_id': d['drink'],
            'drink__crate_size': d['drink__crate_size']
        })

    # merge
    # FIXME: order by id after this
    for a in available_drinks:
        # check if available is not in drinks, add it
        if a.name not in [d['drink__name'] for d in ndrinks]:
            ndrinks.append({
                'drink__name': a.name,
                'drink_sum': '-',
                'drink_id': a.id,
                'drink__crate_size': a.crate_size})

    last_10 = Consumption.objects.filter(user=user_id).order_by('-datetime')[0:10]
    for con in last_10:
        con.count = con.count * -1

    context = {
        'user': user_id,
        'drinks': ndrinks,
        'last_10': last_10,
    }

    return render(request, 'user_detail.html', context)


def remove_consumption(request, consumption_id):
    consumption = get_object_or_404(Consumption, pk=consumption_id)
    user = consumption.user.id
    consumption.delete()

    try:
        to = request.POST['to-view']
        return HttpResponseRedirect(reverse(to))
    except KeyError:
        return HttpResponseRedirect(reverse('beer:user_detail', args=[user]))


def add_consumption(request, count=None):
    user_id = request.POST['user-id']
    user = get_object_or_404(User, pk=user_id)

    # this is so the default is taken for the front page
    try:
        drink_id = request.POST['drink-id']
        drink = Drink.objects.get(pk=drink_id)
    except (KeyError, Drink.DoesNotExist):
        print("!!! drink_id not found")
        drink = Drink.objects.get(pk=1)

    if count:
        Consumption.objects.create(user=user, drink=drink, count=count)
    else:
        Consumption.objects.create(user=user, drink=drink)


@require_POST
def up(request):
    add_consumption(request)
    try:
        to = request.POST['to-view']
        return HttpResponseRedirect(reverse(to, args=[request.POST['user-id']]))
    except KeyError:
        return HttpResponseRedirect(reverse('beer:list'))


@require_POST
def down(request):
    count = request.POST.get('count', -1)
    print("count", count)
    add_consumption(request, count)
    try:
        to = request.POST['to-view']
        return HttpResponseRedirect(reverse(to, args=[request.POST['user-id']]))
    except KeyError:
        return HttpResponseRedirect(reverse('beer:list'))


def last_drinks(request):
    consumptions = Consumption.objects.all().order_by('-datetime')[0:20]

    for con in consumptions:
        con.count = con.count * -1

    context = {
        'consumptions': consumptions,
    }

    return render(request, 'stats.html', context)
