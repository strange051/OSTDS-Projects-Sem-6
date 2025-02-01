from django.shortcuts import render
from .analysis import analyze_data


def dashboard_view(request):
    hist_img, heatmap_img = analyze_data()

    return render(request, 'dashboard.html', {
        'hist_img': hist_img,
        'heatmap_img': heatmap_img
    })
