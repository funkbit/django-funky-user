from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render

from forms import UserChangeForm


@login_required
def edit(request):
    """
    User edit screen example.
    """

    user = request.user

    if request.method == 'POST':

        form = UserChangeForm(request.POST, instance=user)
        if form.is_valid():

            # Update the object
            user = form.save()

            messages.success(request, 'Profile details updated.', fail_silently=True)

            return redirect('user-edit')

    else:

        form = UserChangeForm(instance=user)

    return render(request, 'account/edit.html', {
        'form': form,
    })
