from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review, Petition
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

def index(request):
    search_term = request.GET.get('search')
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        movies = Movie.objects.all()

    template_data = {}
    template_data['title'] = 'Movies'
    template_data['movies'] = movies
    return render(request, 'movies/index.html', {'template_data': template_data})

def show(request, id):
    movie = Movie.objects.get(id=id)
    reviews = Review.objects.filter(movie=movie)
    template_data = {}
    template_data['title'] = movie.name
    template_data['movie'] = movie
    template_data['reviews'] = reviews
    return render(request, 'movies/show.html', {'template_data': template_data})

@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST['comment']!= '':
        movie = Movie.objects.get(id=id)
        review = Review()
        review.comment = request.POST['comment']
        review.movie = movie
        review.user = request.user
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)
    
@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('movies.show', id=id)

    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        return render(request, 'movies/edit_review.html', {'template_data': template_data})
    elif request.method == 'POST' and request.POST['comment'] != '':
        review = Review.objects.get(id=review_id)
        review.comment = request.POST['comment']
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)
    
@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    review.delete()
    return redirect('movies.show', id=id)

def petitions_list(request):
    petitions = Petition.objects.order_by('-created_date').all()
    template_data = {'title': 'Petitions', 'petitions': petitions}
    return render(request, 'movies/petitions.html', {'template_data': template_data})

@login_required
def create_petition(request):
    if request.method == 'GET':
        template_data = {'title': 'Create Petition'}
        return render(request, 'movies/create_petition.html', {'template_data': template_data})
    elif request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        if title == '':
            messages.error(request, 'Title is required')
            return redirect('movies.create_petition')
        p = Petition.objects.create(title = title, description = description, created_by_user = request.user)
        messages.success(request, 'Petition created')
        return redirect('movies.create_petition')
    
@login_required
def vote_petition(request, petition_id):
    petition = get_object_or_404(Petition, id=petition_id)
    if petition.user_voted(request.user):
        petition.votes.remove(request.user)
        messages.info(request, 'Your vote has been removed')
    else:
        petition.votes.add(request.user)
        messages.success(request, 'Your vote has been recorded')
    return redirect('movies.petitions')