from django.shortcuts import render
from django.utils import timezone
from .models import Post
from .models import PostSRR
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from .forms import SrrForm
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
import json

# Create your views here.

def post_list(request):
	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')

	return render(request, 'drug_test/post_list.html', {'posts':posts})


def post_detail(request, pk):
	post = get_object_or_404(Post, pk=pk)

	return render(request, 'drug_test/post_detail.html', {'post': post})


def post_new(request):
	if request.method == "POST":
		form = PostForm(request.POST)

		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.published_date = timezone.now()
			post.save()

		return redirect('post_detail', pk=post.pk)
	else:
		form = PostForm()

	return render(request, 'drug_test/post_edit.html', {'form': form})


def post_edit(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == "POST":
		form = PostForm(request.POST, instance=post)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.published_date = timezone.now()
			post.save()
			return redirect('post_detail', pk=post.pk)
	else:
		form = PostForm(instance=post)

	return render(request, 'drug_test/post_edit.html', {'form': form})



######################################################
## Form for entering SRR identifier

def post_srr(request):
	if request.method == "POST":
		form = SrrForm(request.POST)

		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.created_date = timezone.now()
			post.save()

		return redirect('job_status', pk=post.pk)

	else:
		form = SrrForm()

	return render(request, 'drug_test/job_new.html', {'form': form})	



def update_object_status(post):
	post.dataset_link = 'data/test_example.vcf'
	post.save()

	return post


def job_status(request, pk):

	post = get_object_or_404(PostSRR, pk=pk)

	post = update_object_status(post)

	if post.dataset_link != '':
		return render(request, 'drug_test/job_finished.html', {'post': post})


	return render(request, 'drug_test/job_status.html', {'post': post})




#################

path = r'/home/roma/djangoenv/drug_test/data'
resistance_path = r'/home/roma/djangoenv/drug_test/resistance.json'


def get_med_resistance():
    res = json.load(open(resistance_path))
    result = {}
    for k, v in res.items():
        for v_i in v:
            result[(v_i[0], v_i[1][0], v_i[1][1])] = k

    return result


MED_RESISTANCE = get_med_resistance()


def calc_resistance(inp_data):
    result = []
    for item in inp_data[1:]:
        curr = tuple([int(item[1])] + item[3: 5])
        if curr in MED_RESISTANCE:
            result.append(MED_RESISTANCE[curr])

    return result



def dst_detail(request, pk):
	post = get_object_or_404(PostSRR, pk=pk)

	#filename = post.dataset_link
	filename = 'test_example.vcf'

	data = open('{}/{}'.format(path, filename)).readlines()
	data = list(map(lambda x: x.split('\t'), data[42:]))
	resistance_items = ', '.join(calc_resistance(data))

	data_res = []
	for item in data[1:]:
		curr = tuple([int(item[1])] + item[3: 5])
		if curr in MED_RESISTANCE:
			data_res.append(item[1:])


	return render(request, 'drug_test/dst_detail.html', {'post': post, 'data': data_res, 'resistance_items': resistance_items})

