from django.http import JsonResponse


def angular_ajax_test(request):
    data = [
        {
            "url": 'http://dragonball.wikia.com/wiki/Goku',
            "title": '[AJAX] GOKU - The Legendary Super Saiyyan from DRAGONBALL Z',
            "image": 'https://qph.ec.quoracdn.net/main-qimg-2daa8ad430ff8f374e4c0a34796c05c6.webp'
        },
        {
            "url": 'http://dragonball.wikia.com/wiki/Vegeta',
            "title": '[AJAX] Vegeta - The prince of the fallen Saiyan race, the older brother of Goku',
            "image": 'https://img00.deviantart.net/e3d0/i/2009/177/9/e/super_vegeta_cool_wallpaper_by_bardock85.png'
        },
        {
            "url": 'http://dragonball.wikia.com/wiki/Chi-Chi',
            "title": '[AJAX] Chi-Chi - The princess of Fire Mountain and the daughter of the Ox-King who later marries Goku',
            "image": 'https://static.comicvine.com/uploads/original/11122/111223595/4476845-1442409759-36664.png'
        },

        {
            "url": 'http://dragonball.wikia.com/wiki/Master_Roshi',
            "title": '[AJAX] Master Roshi - A master of martial arts, who trained Gohan, Ox-King, Goku, Krillin, and Yamcha',
            "image": 'https://i.imgur.com/FPkaKZY.jpg'
        },
        {
            "url": 'http://dragonball.wikia.com/wiki/Ox-King',
            "title": '[AJAX] Ox-King - The king of Fire Mountain, as well as the father of Chi-Chi, the father in-law of Goku',
            "image": 'https://vignette2.wikia.nocookie.net/teamfourstar/images/2/24/Ox-King-psd61345.png/revision/latest?cb=20130627212350'
        },
        {
            "url": 'http://dragonball.wikia.com/wiki/Krillin',
            "title": '[AJAX] Krillin -  One of the most powerful and talented Human martial artists on Earth, a close friend of Goku',
            "image": 'https://vignette3.wikia.nocookie.net/anime-pedia/images/c/cc/Kid_krillin_peace.jpg/revision/latest?cb=20120217232535'
        },
        {
            "url": 'http://tutorialzine.com/2013/04/services-chooser-backbone-js/',
            "title": '[AJAX] Yamcha - A very talented martial artist and one of the most powerful humans on Earth, a close friend of Goku',
            "image": 'http://vignette3.wikia.nocookie.net/deathbattlefanon/images/5/54/Yamcha.png/revision/latest?cb=20150317171234'
        }]
    response = JsonResponse({'items': data})
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'GET'
    response['Access-Control-Allow-Headers'] = 'Origin, Content-Type, X-Auth-Token, X-Requested-With'
    return response
