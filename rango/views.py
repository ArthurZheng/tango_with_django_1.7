from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, render_to_response
from django.http.response import HttpResponseRedirect, HttpResponse
from .models import Category, Page
from .forms import CategoryForm, PageForm, UserProfileForm, UserForm


def index(request):
    # category_list = Category.objects.order_by('-likes')[:5]
    # page_list = Page.objects.order_by('-views')[:5]

    category_list = Category.objects.order_by('-likes')[:5]

    # set up test cookie;
    request.session.set_test_cookie()

    # setting up session to track number of visits of a visitor
    visits = request.session.get('visits')
    # If visits doesn't exist/ if the user hasn't visited
    if not visits:
        visits = 1

    reset_last_visit_time = False

    last_visit = request.session.get('last_visit')

    if last_visit:
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

        if (datetime.now() - last_visit_time).seconds > 0:
            # reassign the value of the coolike to +1 of what it was before.
            visits += 1
            # update the last visit cookie too.
            reset_last_visit_time = True
    else:
    # cookie last visit doesn't exist, so create it to the current date/time
        reset_last_visit_time = True

    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits

    return render(request, 'rango/index.html', {'category_list':category_list, 'visits':visits})
    # return render_to_response('rango/index.html', {'category_list':category_list})


def about(request):
    # get the value of visits from request.session
    visits = request.session.get('visits')
    # if there is no value in visits/ False
    if not visits:
        # declare and initialize visits = 1
        visits = 1

    # get the value (time) of the last_visit from request.session (the time visitor last visited the page)
    last_visit = request.session.get('last_visit')
    # set up a flag Boolean variable to determine if we need to update last_visit time
    update_last_visit_time = False

    # if there's a last_visit/ visitor visited the page
    if last_visit:
        # get the datetime when the visitor visited the page
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")
        # get the time difference between now and the last visit, and test to see if the difference is greater than 0;
        # we can change 0 to 5 minutes or 24 hours if we need to
        if (datetime.now() - last_visit_time).seconds > 0:
            # update the visit time
            visits += 1
            # change the flag to say we need to update the last visit time
            update_last_visit_time = True
    # the visitor hasn't visited the page yet, we'll set up their first visit by setting up the 'last_visit' value in the next step.
    else:
        # if they haven't visited yet, we'll take it as we need to update their last visit time
        update_last_visit_time = True

    # if we need to reset/update last visit time
    if update_last_visit_time:
        # update both last_visit/ visits in the request.session dictionary
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits

    return render(request, 'rango/about.html', {'about' : "Rango says this is the about page", 'visits': visits})
    # return render_to_response('rango/about.html', {'about': "Rango says this is AbOuT Page"})


def detail(request, category_id):
    cat = get_object_or_404(Category, pk=category_id)
    return render(request, 'rango/detail.html', {'category':cat})
    # return render_to_response('rango/detail.html', {'category':cat})


def category(request, category_name_slug):
    cat = Category.objects.get(slug = category_name_slug)

    try:
        pages = Page.objects.filter(category=cat)

    except (KeyError, Page.DoesNotExist):
        pass
    return render(request, 'rango/category.html', {'category_name': cat.name, 'pages':pages, 'category': cat})
    # return render_to_response('rango/category.html', {'category_name':cat.name, 'pages': pages, 'category':cat })


def like(request, category_id):
    cat = get_object_or_404(Category, pk=category_id)
    cat.likes += 1
    cat.save()

    return HttpResponseRedirect(reverse('rango:detail2', args=(cat.id,)))
    # return HttpResponseRedirect('/rango/')


@login_required
def increaseView(request, category_id):
    try:
        cate = Category.objects.get(pk = request.POST['category'])
    except (KeyError, Category.DoesNotExist):
        return index(request)
    else:
        cate.views += 10
        cate.save()
    return HttpResponseRedirect('/rango/')


@login_required
def increaseLike(request, category_id):
    categ = get_object_or_404(Category, pk=category_id)

    try:
        likeNumber = request.POST['likes']
    except (KeyError):
        return index(request)
    else:
        likeNumber = int(likeNumber)
        if likeNumber <= 0:
            likeNumber = 0
        else:
            categ.likes += likeNumber
            categ.save()
    return HttpResponseRedirect('/rango/')


@login_required
def increaseDetailView(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    try:
        page = category.page_set.get(pk = request.POST['views'])
    except (KeyError, Page.DoesNotExist):
        return render(request,'rango/detail.html',{'category':category, 'error_message': "Sorry, you didn't select a views."})
    else:
        page.views += 5
        page.save()
    return HttpResponseRedirect(reverse('rango:category', args=(category.id,)))


@login_required
def add_category(request):

    # test to see if the user is logged in using the user object provided by the request context
    if not request.user.is_authenticated():
        return HttpResponse('You are not logged in.')
    else:
        # A Http POST?
        if request.method == 'POST':
            form = CategoryForm(request.POST)
            # Have form been provided with a valid form?
            if form.is_valid():
                #Save the new category to the database
                form.save(commit=True)

                #Now call the index() view.
                return index(request)

            else:
                #The supplied form contained errors, print them to the terminal
                print form.errors

        else:
            #if the method is not POST, display the form to enter details
            form = CategoryForm()

        return render(request, 'rango/add_category.html', {'form': form})


@login_required
def add_page(request, category_name_slug):
    try:
        cat  = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        cat = None

    #check if it's a post
    if request.method == 'POST':
        form = PageForm(request.POST)
        # have form been provided with a valid form?
        if form.is_valid():
            # save the new page to the db
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()

            # return detail(request, cat.id)
            return HttpResponseRedirect(reverse('rango:detail2', args=(cat.id, )))
        else:
            print form.errors

    else:
        # if method is not POST, display the form to enter details
        form = PageForm()

    return render(request, 'rango/add_page.html',  {'form':form, 'category':cat})


def register(request):

    if request.session.test_cookie_worked():
        print ">>> TEST COOKIE WORKED!"

    # A boolean value for telling the template if registration successful.
    # Set to False initially. Code changes value to True if registration successful.
    registered = False

    # if it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        # If the two forms are valid..
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to db
            user = user_form.save()

            # Now we hash the password with the set_password method
            # Once hashed, we can update the user object
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance
            # Since we need to set the user attribute ourselves, we set to commit = False
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user # associate the user with user profile info

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now save the UserProfile instance
            profile.save()

            registered = True # update the registered variable to tell the template registration was successful.

            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            # They will also be shown to the user
        else:
            print  user_form.errors, profile_form.errors

    # Not a Http POST, so we render our form using the two ModelForm instances.
    # These forms will be blank, ready for user input
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request, 'rango/register.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


def user_login(request):
    # If the method is POST, try to pull out the relevant information
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        # We use the request.POST.get('<variable>') as opposed to request.POST['<variable>'],
        # because the request.POST.get('<variable>') returns None, if the value does not exist
        # while the request.POST['<variable>'] will raise KeyError exception
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Uses Django's machinery to attempt to see if the username/password combination is valid - a User object is returned if it is.
        user = authenticate(username = username, password = password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absense of a value), no user with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage
                login(request, user)
                return HttpResponseRedirect('/rango/')
            else:
                # An inactive account was used -- no logging in!
                return HttpResponse("Your Rango account was disabled said Rango Jiangli.")
        else:
            # Bad login details were provided. So we can't log the user in.

            error_message = "Invalid login details: username: {0} -- password: {1} doesn't match".format(username, password)
            print error_message
            print "Invalid login details supplied said Rango Jun."

            return render(request, 'rango/login.html', {'error_message': error_message, 'username':username, 'password': password})

    # Not a HTTP POST, so display the login form.
    else:
        # No context variable to pass to the template system, hence the blank dictionary object..
        return render(request, 'rango/login.html', {})


# Demonstrating the use of @login_required decorator
@login_required
def restricted(request):
    print "Inside restricted view"
    return HttpResponse("Since you are logged in, you can see this.")


# using the login_required decorator to ensure only those who logged in can access this view
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can log them out using Django's django.contrib.auth.logout
    logout(request)
    # take the user back to homepage
    return HttpResponseRedirect('/rango/')

