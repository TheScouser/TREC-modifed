import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TREC.settings')
django.setup()

from django.contrib.auth.models import User
from treco.models import Track, Task, Run, Researcher
from treco.invoker import *

def populate():

    add_researcher('bob', 'bob', 'bob@researcher.gla.ac.uk', 'profile_pictures/default.png', 'www.gla.ac.uk', 'bob', 'Glasgow University', False)
    add_researcher('jen', 'jen', 'jen@researcher.gla.ac.uk', 'profile_pictures/default.png', 'www.gla.ac.uk', 'jen', 'Glasgow University', False)
    add_researcher('jill', 'jill', 'jill@admin.gla.ac.uk', 'profile_pictures/default.png', 'www.gla.ac.uk', 'jill', 'Glasgow University', True)
    asu = add_researcher('ASU', 'ASU', 'asu@researcher.as.ac.uk', 'profile_pictures/default.png', 'www.as.ac.uk', 'Alpha Team', 'AS University', False)
    ck = add_researcher('CK', 'CK', 'ck@researcher.ck.ac.uk', 'profile_pictures/default.png', 'www.ck.ac.uk', 'Chaos and Kontrol', 'CK University', False)
    hk = add_researcher('HK', 'HK', 'hk@researcher.hk.ac.uk', 'profile_pictures/default.png', 'www.hk.ac.uk', 'HongKongIR', 'HK University', False)
    ict = add_researcher('ICT', 'ICT', 'ict@researcher.ict.ac.uk', 'profile_pictures/default.png', 'www.ict.ac.uk', 'ICTer', 'University of ICT', False)
    rim = add_researcher('RIM', 'RIM', 'rim@researcher.rim.ac.uk', 'profile_pictures/default.png', 'www.rim.ac.uk', 'IRJobs', 'Royal Institute of Mayhem', False)

    add_track('Robust2004', 'http://trec.nist.gov/data/t13_robust.html', 'News Retrieval', 'News')
    rob2005 = add_track('Robust2005', 'http://trec.nist.gov/data/t14_robust.html', 'News Retrieval', 'News')
    add_track('MillionQuery', 'http://ciir.cs.umass.edu/research/million/', 'Million Query Track', 'Web')
    web2005 = add_track('Terabyte', 'http://www-nlpir.nist.gov/projects/terabyte/', 'Terabyte Web Track', 'Web')
    apnews = add_track('APNews', '', 'News Retrieval Track', 'News')

    robTask = add_task(rob2005, 'Ad Hoc Topic Retrieval', 'http://trec.nist.gov/data/t14_robust.html', 'For each topic find all the relevant documents', 2005, 'judgement_files/aq.trec2005.qrels')
    add_task(web2005, 'Ad Hoc Topic Retrieval', 'http://www-nlpir.nist.gov/projects/terabyte/', 'Find all the relevant web pages', 2005, 'judgement_files/dg.trec.qrels')
    add_task(apnews, 'Ad Hoc Topic Retrieval', '', 'Find all the relevant news articles', 2001, 'judgement_files/ap.trec.qrels')

    results = getResults(invoke('media/judgement_files/aq.trec2005.qrels', 'media/result_files/input.ASUBE'))
    add_run(asu, robTask, 'AS First', 'AS First run.', 'result_files/input.ASUBE', 0, 0, 0, results['map'], results['P_10'], results['P_20'])
    results = getResults(invoke('media/judgement_files/aq.trec2005.qrels', 'media/result_files/input.ASUBE3'))
    add_run(asu, robTask, 'AS Second', 'AS Second run.', 'result_files/input.ASUBE3', 0, 0, 0, results['map'], results['P_10'], results['P_20'])
    results = getResults(invoke('media/judgement_files/aq.trec2005.qrels', 'media/result_files/input.ASUDE'))
    add_run(asu, robTask, 'AS Third', 'AS Third run.', 'result_files/input.ASUDE', 0, 0, 0, results['map'], results['P_10'], results['P_20'])

    results = getResults(invoke('media/judgement_files/aq.trec2005.qrels', 'media/result_files/input.CKonD'))
    add_run(ck, robTask, 'CK First', 'CK First run.', 'result_files/input.CKonD', 1, 1, 1, results['map'], results['P_10'], results['P_20'])
    results = getResults(invoke('media/judgement_files/aq.trec2005.qrels', 'media/result_files/input.CKSEonD'))
    add_run(ck, robTask, 'CK Second', 'CK Second run.', 'result_files/input.CKSEonD', 1, 1, 1, results['map'], results['P_10'], results['P_20'])
    results = getResults(invoke('media/judgement_files/aq.trec2005.qrels', 'media/result_files/input.CKSEonTSE'))
    add_run(ck, robTask, 'CK Third', 'CK Third run.', 'result_files/input.CKSEonTSE', 1, 1, 1, results['map'], results['P_10'], results['P_20'])

    results = getResults(invoke('media/judgement_files/aq.trec2005.qrels', 'media/result_files/input.HKPU2CT'))
    add_run(hk, robTask, 'HK First', 'HK First run.', 'result_files/input.HKPU2CT', 1, 2, 2, results['map'], results['P_10'], results['P_20'])
    results = getResults(invoke('media/judgement_files/aq.trec2005.qrels', 'media/result_files/input.HKPU2CTDN'))
    add_run(hk, robTask, 'HK Second', 'HK Second run.', 'result_files/input.HKPU2CTDN', 1, 2, 2, results['map'], results['P_10'], results['P_20'])
    results = getResults(invoke('media/judgement_files/aq.trec2005.qrels', 'media/result_files/input.HKPUCD'))
    add_run(hk, robTask, 'HK Third', 'HK Third run.', 'result_files/input.HKPUCD', 1, 2, 2, results['map'], results['P_10'], results['P_20'])

    results = getResults(invoke('media/judgement_files/aq.trec2005.qrels', 'media/result_files/input.ICT05qerfD'))
    add_run(ict, robTask, 'ICT First', 'ICT First run.', 'result_files/input.ICT05qerfD', 0, 3, 3, results['map'], results['P_10'], results['P_20'])
    results = getResults(invoke('media/judgement_files/aq.trec2005.qrels', 'media/result_files/input.ICT05qerfDg'))
    add_run(ict, robTask, 'ICT Second', 'ICT Second run.', 'result_files/input.ICT05qerfDg', 0, 3, 3, results['map'], results['P_10'], results['P_20'])
    results = getResults(invoke('media/judgement_files/aq.trec2005.qrels', 'media/result_files/input.ICT05qerfT'))
    add_run(ict, robTask, 'ICT Third', 'ICT Third run.', 'result_files/input.ICT05qerfT', 0, 3, 3, results['map'], results['P_10'], results['P_20'])

    results = getResults(invoke('media/judgement_files/aq.trec2005.qrels', 'media/result_files/input.RIMam05d200'))
    add_run(rim, robTask, 'RIM First', 'RIM First run.', 'result_files/input.RIMam05d200', 0, 4, 1, results['map'], results['P_10'], results['P_20'])
    results = getResults(invoke('media/judgement_files/aq.trec2005.qrels', 'media/result_files/input.RIMam05l050'))
    add_run(rim, robTask, 'RIM Second', 'RIM Second run.', 'result_files/input.RIMam05l050', 0, 4, 1, results['map'], results['P_10'], results['P_20'])
    results = getResults(invoke('media/judgement_files/aq.trec2005.qrels', 'media/result_files/input.RIMam05l200'))
    add_run(rim, robTask, 'RIM Third', 'RIM Third run.', 'result_files/input.RIMam05l200', 0, 4, 1, results['map'], results['P_10'], results['P_20'])

    # Print out what we have added to the user.
    for c in Track.objects.all():
        for p in Task.objects.filter(track=c):
            print "- {0} - {1}".format(str(c), str(p))


def add_track(title, url, description, genre):
    t = Track.objects.get_or_create(track_title=title, track_url=url, description=description, genre=genre)[0]
    t.save()
    return t


def add_task(track, title, task_url, description, year, judgement_file):
    t = Task.objects.get_or_create(track=track, title=title, task_url=task_url, description=description,
                                   year=year, judgement_file=judgement_file)[0]
    t.save()
    return t


def add_run(researcher, task, name, description, result_file, run_type, query_type, feedback_type, map, p10, p20):
    r = Run.objects.get_or_create(researcher=researcher, task=task, name=name, description=description,
                                  result_file=result_file, run_type=run_type, query_type=query_type,
                                  feedback_type=feedback_type, map=map, p10=p10, p20=p20)[0]
    r.save()
    return r


def add_researcher(username, password, email, profile_picture, website, display_name, organization, admin):
    if admin:
        u = User.objects.create_superuser(username, email, password)
    else:
        u = User.objects.create_user(username=username, password=password, email=email)
    r = Researcher.objects.get_or_create(userid=u, profile_picture=profile_picture, website=website, display_name=display_name,
                                         organization=organization)[0]
    u.save()
    r.save()
    return r


# Start execution here!
if __name__ == '__main__':
    print "Starting Rango population script..."
    populate()