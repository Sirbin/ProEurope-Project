from django.shortcuts import render



def page_not_found(request):
    context = {}
    return render(request,'pageErrors/page-404.html',context=context,status=404)


def page_error(request):
    context = {}
    return render(request, 'pageErrors/page-500.html', context=context, status=500)