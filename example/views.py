import random
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404, HttpResponse
from django.contrib import messages
from django.contrib.auth import login
from accounts.forms import *
from exams.forms import *
from institutes.models import Modules
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def home_view(request):
    if not request.user.is_authenticated() or request.user.type != 'teacher':
        return redirect('login')
    else:

        # Sifre kontrolu
        user = authenticate(username=request.user.username, password="12345678")
        if user:
            return redirect("teacher:change_password")

        # Activated Modules
        institute = get_object_or_404(Institute, id=request.user.instituteid.id)
        active = list(institute.modules.all().values('name'))
        allmodules = list(Modules.objects.all().values('name'))

        def comp(list1, list2):
            list = []
            for val in list1:
                if not val in list2:
                    list.append(val)
            return list

        notactive = comp(allmodules, active)

        # Control statüsünde olan sınavları getir
        exams = Exams.objects.filter(instituteid=request.user.instituteid).order_by('-start_date')[:3]
        exams_list = list()
        exams_list_control = list()
        for exam in exams:
            if exam.status == "control":
                exams_list.append(exam)

        # Kontrol listesini çek ve öğretmenin kontrol edeceği sınavları seç
        for exam in exams_list:
            control_list = ExamControlList.objects.filter(exam_id=exam.id, teacher_ids__in=[request.user]) # Her ogrenci için bir tane kayıt var
            if len(list(control_list)) > 0:
                exams_list_control.append(exam)


        context = {'active': active, 'notactive': notactive, 'control_exams':exams_list_control}
        return render(request, "teacher/index.html", context)


def change_password_view(request):
    if not request.user.is_authenticated() or request.user.type != 'teacher':
        return redirect('login')
    else:
        form = ChangePasswordForm(request.POST or None)
        if form.is_valid():
            user = get_object_or_404(MyUser, id=request.user.id)
            user.set_password(form.cleaned_data["password"])
            user.save()
            user_login = authenticate(username=request.user.username, password=form.cleaned_data["password"])
            login(request, user_login)
            messages.success(request, "You have successfully changed password.")
            return redirect('teacher:index')
        context = {'form': form}
        return render(request, "teacher/change_password.html", context)



# MY EXAMS

def create_exam(form, request, id):
    if not id:
        # Yeni Kayıt
        data = Exams()
    else:
        # Düzenleme - Eski kayıtı sil ve yerine kayıt oluştur
        data = get_object_or_404(Exams, id=id)
        data.delete()
        data = Exams()
        data.id = id


    # Ortak Bilgileri Kaydet
    data.module = form.cleaned_data.get('module')
    data.category = form.cleaned_data.get('category')
    tz = pytz.timezone("Europe/Istanbul")
    start_date = datetime.datetime.strptime(form.cleaned_data.get('start_date'), '%d.%m.%Y, %H:%M')
    data.start_date = tz.localize(start_date, is_dst=None)
    data.createdby = request.user
    data.question = form.cleaned_data.get("questions")
    data.instituteid = request.user.instituteid

    # Module ozel field'ler
    if data.module.name == "Speaking":
        data.control_by = form.cleaned_data.get("control_choices") # Own - Other
        data.questions_count = form.cleaned_data.get("question_count")
        data.control_time = form.cleaned_data.get("control_time")
        data.question_split = form.cleaned_data.get("question_split") # Same or No
        data.finish_date = datetime.datetime.strptime(form.cleaned_data.get('finish_date'), '%d.%m.%Y, %H:%M')
        data.rubric_id = form.cleaned_data.get('rubric_speaking')

    elif data.module.name == "Writing":
        data.control_by = form.cleaned_data.get("control_choices") # Own - Other
        data.questions_count = form.cleaned_data.get("question_count")
        data.control_time = form.cleaned_data.get("control_time")
        data.question_split = form.cleaned_data.get("question_split") # Same or No
        data.writing_feedback = form.cleaned_data.get("writing_feedback")
        data.finish_date = datetime.datetime.strptime(form.cleaned_data.get('finish_date'), '%d.%m.%Y, %H:%M')
        data.rubric_id = form.cleaned_data.get('rubric_writing')

    elif data.module.name == "Live Speaking":
        data.rubric_id = form.cleaned_data.get('rubric_speaking')

    data.save()
    exam = get_object_or_404(Exams, id=data.id)
    exam.classes = form.cleaned_data.get('classes')
    exam.save()



    # - DB.Exam kaydet, Show sayfasında göstermek için -7
    if data.module.name != "Live Speaking":
        control_choices = form.cleaned_data.get("control_choices")

        # OGRETMENLER
        if control_choices == "own":
            exam.control_list.add(request.user)

        elif control_choices == "other":
            control_count = form.cleaned_data.get("control_count")
            control_teachers = form.cleaned_data.get("control_teachers")
            exam.control_list = control_teachers
            exam.control_count = control_count

        question_choice = form.cleaned_data.get("questions") # random or specific

        # SORULAR
        if question_choice == "specific":
            if data.module.name == "Speaking":
                exam.question_list = form.cleaned_data.get("specific_questions_speaking")
                exam.save()
            elif data.module.name == "Writing":
                exam.question_list = form.cleaned_data.get("specific_questions_writing")
                exam.save()
        else:
            exam.save()
        



    # // EXAM CONTROL LIST //

    # Her ogrenci icin ogretmen ve soru belirlemek icin
    # Ogrenci listesini cek ve donguye sok

    # Seçilen sınıflardaki öğrencileri tek listeye ekle
    student_list = list()
    for classes in list(form.cleaned_data.get('classes')):
        q = MyUser.objects.filter(instituteid=request.user.instituteid, type="student", classids=classes)
        student_list += list(q)

    teacher_index = 1  # Ogretmen dagitirken modunu almak icin

    if data.module.name != "Live Speaking":
        for student in student_list:  # Her ogrenci icin islemler

            # OGRETMEN DAGITMA

            control_choices = form.cleaned_data.get("control_choices")
            teacher_list = list()

            if control_choices == "own":
                teacher_list.append(request.user)

            elif control_choices == "other":
                control_count = form.cleaned_data.get("control_count")
                control_teachers = form.cleaned_data.get("control_teachers")

                if len(list(control_teachers)) == control_count:
                    teacher_list += list(control_teachers)

                elif len(list(control_teachers)) > control_count:
                    for i in range(0, control_count):
                        teacher_list.append(list(control_teachers)[(teacher_index % len(list(control_teachers)))])
                        teacher_index += 1

            # SORU DAGITMA

            question_choice = form.cleaned_data.get("questions") # random or specific
            question_count = form.cleaned_data.get("question_count") # kaç tane soru
            question_split = form.cleaned_data.get("question_split") # aynı soru mu farklı soru mu
            question_list = list()

            # Hangi sorular sorulacak belirle

            if question_choice == "random":
                question_list_random_set = list(ExamQuestions.objects.filter(module=data.module, instituteid=request.user.instituteid))
            elif question_choice == "specific":
                if data.module.name == "Speaking":
                    question_list_set = list(form.cleaned_data.get("specific_questions_speaking"))
                elif data.module.name == "Writing":
                    question_list_set = list(form.cleaned_data.get("specific_questions_writing"))


            # - Ogrenciye soru dağıtmaya başla -
            # Her ogrenciye aynı soru
            if question_split == "yes":

                # Karısık sorulardan count kadar sec
                question_list_set = list()
                if question_choice == "random":
                    random_list = random.sample(range(0, len(question_list_random_set)), question_count)
                    for i in random_list:
                        question_list_set.append(question_list_random_set[i])

                question_list = question_list_set


            # Her ogrenciye farklı soru
            else:

                # Random listesin boyutu kadar
                if question_choice == "random":
                    random_list = random.sample(range(0, len(question_list_random_set)), question_count)
                    for i in random_list:
                        question_list.append(question_list_random_set[i])


                # Seçilen soru listesinin boyutu kadar
                else:
                    random_list = random.sample(range(0, len(question_list_set)), question_count)
                    for i in random_list:
                        question_list.append(question_list_set[i])

            control_data = ExamControlList()
            control_data.exam_id = exam
            control_data.instituteid = request.user.instituteid
            control_data.student_id = student
            control_data.save()

            inst_data = get_object_or_404(ExamControlList, id=control_data.id)
            inst_data.question_ids = question_list
            inst_data.teacher_ids = teacher_list
            inst_data.save()


def my_exams_view(request):
    if not request.user.is_authenticated() or request.user.type != 'teacher':
        return redirect('login')
    else:
        data = Exams.objects.filter(instituteid=request.user.instituteid, createdby=request.user).order_by('-start_date')
        context = {'data': data, 'active_tab': 'my_exams'}
        return render(request, "teacher/my_exams_list.html", context)


def my_exams_update_view(request, id):
    if not request.user.is_authenticated() or request.user.type != 'teacher':
        return redirect('login')
    else:
        data = get_object_or_404(Exams, id=id)

        local_tz = pytz.timezone('Europe/Istanbul')

        def utc_to_local(utc_dt):
            local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
            return local_tz.normalize(local_dt)

        start_date = utc_to_local(data.start_date).strftime('%d.%m.%Y, %H:%M')


        # Gelen Bilgileri Manueal Manuel Olarak Forma Gönder
        finish_date = None
        control_time = None
        question_count = None
        question_split = None
        questions = None
        control_choices = None
        control_count = None
        writing_feedback = None

        if data.finish_date:
            finish_date = utc_to_local(data.finish_date).strftime('%d.%m.%Y, %H:%M')
        if data.control_time:
            control_time = data.control_time
        if data.questions_count:
            question_count = data.questions_count
        if data.question_split:
            question_split = data.question_split
        if data.question:
            questions = data.question
        if data.control_by:
            control_choices = data.control_by
        if data.control_count:
            control_count = data.control_count
        if data.writing_feedback:
            writing_feedback = data.writing_feedback

        init = {'module': data.module, 'category': data.category, 'classes': data.classes.all(),
                'start_date': start_date, 'finish_date': finish_date, 'control_time': control_time,
                'question_count':question_count, 'question_split':question_split, 'questions':questions,
                'control_count':control_count, 'control_choices':control_choices, 'writing_feedback':writing_feedback,}

        if data.question_list:
            if data.module.name == "Speaking":
                init['specific_questions_speaking'] = data.question_list.all()
            elif data.module.name == "Writing":
                init['specific_questions_writing'] = data.question_list.all()
        if data.control_list:
            init['control_teachers'] = data.control_list.all()

        
        form = ExamForm(request.POST or None, user=request.user, initial=init)

        if form.is_valid():
            create_exam(form=form, request=request, id=data.id)

            messages.success(request, "Successful")
            return redirect('teacher:my_exams')

        context = {'form': form, 'active_tab': 'my_exams', 'start_date': start_date, 'id': data.id}
        return render(request, "teacher/create_exam_form.html", context)


def my_exams_delete_view(request, id):
    if not request.user.is_authenticated() or request.user.type != 'teacher':
        return redirect('login')
    else:
        data = get_object_or_404(Exams, id=id)
        data.delete()
        messages.success(request, "Successful")
        return redirect('teacher:my_exams')


def my_exams_show_view(request, id):
    if not request.user.is_authenticated() or request.user.type != 'teacher':
        return redirect('login')
    else:
        data = get_object_or_404(Exams, id=id)
        context = {'data': data, 'active_tab': 'my_exams'}
        return render(request, "teacher/exam_show.html", context)




# CONTROL EXAM

def control_exam_view(request):
    if not request.user.is_authenticated() or request.user.type != 'teacher':
        return redirect('login')
    else:

        # Control statüsünde olan sınavları getir
        exams = Exams.objects.filter(instituteid=request.user.instituteid).order_by('-start_date')
        exams_list = list()
        exams_list_control = list()
        for exam in exams:
            if exam.status == "control":
                exams_list.append(exam)

        # Kontrol listesini çek ve öğretmenin kontrol edeceği sınavları seç
        for exam in exams_list:
            control_list = ExamControlList.objects.filter(exam_id=exam.id, teacher_ids__in=[request.user]) # Her ogrenci için bir tane kayıt var
            if len(list(control_list)) > 0:
                exams_list_control.append(exam)

        context = {'exams_list': exams_list_control, 'active_tab':'control_exam'}
        return render(request, "teacher/control_exam.html", context)


def control_exam_list_view(request, id):
    if not request.user.is_authenticated() or request.user.type != 'teacher':
        return redirect('login')
    else:

        # Exam ID'den sınavı getir ve kontrol edilecek öğrencileri listele
        exam = get_object_or_404(Exams, id=id)
        count = get_list_or_404(ExamControlList, exam_id=exam.id)
        exam.count = count[0].question_ids.all().count()

        student_list = list()
        control_list = ExamControlList.objects.filter(exam_id=id, teacher_ids__in=[request.user]).order_by('student_id') # Her ogrenci için soru sayısı kadar kayıt var
        for data in control_list:
            # Not verildiyse öğrenci bilgisine ekle
            points_total = ExamTotalPointList.objects.filter(instituteid=request.user.instituteid, exam_id=id, teacher_id=request.user, student_id=data.student_id)
            if points_total.count() > 0:
                data.student_id.point = str(points_total[0].point)
            student_list.append(data.student_id)
            
        context = {'student_list': student_list, 'active_tab':'control_exam', 'exam': exam}
        return render(request, "teacher/control_exam_list.html", context)




# CREATE EXAM

def exam_create_view(request):
    if not request.user.is_authenticated() or request.user.type != 'teacher':
        return redirect('login')
    else:
        form = ExamForm(request.POST or None, user=request.user)
        if form.is_valid():
            create_exam(form=form, request=request, id=None)

            messages.success(request, "You have successfully created it.")
            return redirect('teacher:my_exams')
        context = {'form': form, 'active_tab': 'create_exam', 'id': None}
        return render(request, "teacher/create_exam_form.html", context)



# POINTS

def points_view(request):
    if not request.user.is_authenticated() or request.user.type != 'teacher':
        return redirect('login')
    else:
        
        # Exams - Her sınıf için ayrı sorgula ve kayıtları birleştir
        exams = list()
        for classes in list(request.user.classids.all()):
            exams_all = Exams.objects.filter(instituteid=request.user.instituteid, classes__in=[classes]).order_by('-start_date')
            for exam in exams_all:
                if exam.status == "done":
                    exams.append(exam)
        
        # Tekar eden kayıtları sil
        exams = list(set(exams)) 

        context = {'active_tab': 'points', 'exams':exams}
        return render(request, "teacher/points.html", context)


def points_list_view(request, id):
    if not request.user.is_authenticated() or request.user.type != 'teacher':
        return redirect('login')
    else:
        
        # Exam ID'den sınavı getir ve sınava giren öğrencileri bul
        exam = get_object_or_404(Exams, id=id)
        control_list = ExamControlList.objects.filter(exam_id=exam.id).order_by('student_id')
        exam.count = control_list[0].question_ids.all().count()

        student_list = list()
        for single in control_list:
            # Öğrenciye sınavda verilen notlar / Kontrol eden öğretmen sayısı kadar
            points_total = ExamTotalPointList.objects.filter(instituteid=request.user.instituteid, exam_id=id, student_id=single.student_id)
            total = 0
            if points_total.count() > 0:
                for i in points_total:
                    total += int(i.point)
                total = int(total / points_total.count())
            single.student_id.point = total
            student_list.append(single.student_id)

        # for data in control_list:
        #     # Not verildiyse getir
        
        #     if points_total.count() > 0:
        #         data.student_id.point = str(points_total[0].point)
        #     student_list.append(data.student_id)

        context = {'student_list': student_list, 'active_tab':'points', 'exam': exam}
        return render(request, "teacher/points_list.html", context)

# QUESTIONS

def questions_view(request):
    if not request.user.is_authenticated() or request.user.type != 'teacher':
        return redirect('login')
    else:
        my_questions = ExamQuestions.objects.filter(instituteid=request.user.instituteid, createdby=request.user)
        all_questions = ExamQuestions.objects.filter(instituteid=request.user.instituteid).exclude(
            createdby=request.user).distinct()
        context = {'all_data': all_questions, 'my_data': my_questions, 'active_tab': 'questions'}
        return render(request, "teacher/exam_question_list.html", context)


def questions_create_view(request):
    if not request.user.is_authenticated() or request.user.type != 'teacher':
        return redirect('login')
    else:
        form = ExamQuestionsForm(request.POST or None, user=request.user)
        if form.is_valid():
            data = form.save(commit=False)
            data.createdby = request.user
            data.instituteid = request.user.instituteid
            data.save()
            messages.success(request, "You have successfully created it.")
            return redirect('teacher:questions')
        context = {'form': form, 'active_tab': 'questions'}
        return render(request, "teacher/exam_question_form.html", context)


def questions_update_view(request, id):
    if not request.user.is_authenticated() or request.user.type != 'teacher':
        return redirect('login')
    else:
        data = get_object_or_404(ExamQuestions, id=id)
        form = ExamQuestionsForm(request.POST or None, instance=data, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Successful")
            return redirect('teacher:questions')
        context = {'form': form, 'active_tab': 'questions'}
        return render(request, "teacher/exam_question_form.html", context)


def questions_delete_view(request, id):
    if not request.user.is_authenticated() or request.user.type != 'teacher':
        return redirect('login')
    else:
        data = get_object_or_404(ExamQuestions, id=id)
        data.delete()
        messages.success(request, "Successful")
        return redirect('teacher:questions')


def questions_show_view(request, id):
    if not request.user.is_authenticated() or request.user.type != 'teacher':
        return redirect('login')
    else:
        data = get_object_or_404(ExamQuestions, id=id)
        context = {'data': data, 'active_tab': 'questions'}
        return render(request, "teacher/exam_question_show.html", context)



# PERSONAL

def personal_settings_view(request):
    if not request.user.is_authenticated() or request.user.type != 'teacher':
        return redirect('login')
    else:
        data = get_object_or_404(MyUser, id=request.user.id)
        form = PersonalSettingsForm(request.POST or None, request.FILES or None, instance=data)
        if form.is_valid():

            user = form.save(commit=False)
            paw = form.cleaned_data.get('password')
            if paw:
                user.set_password(paw)
                messages.success(request, "Successful. Your password has been changed.")
            else:
                messages.success(request, "Successful")
            user.save()
            user_login = authenticate(username=request.user.username, password=paw)
            login(request, user_login)

            return redirect('manager:index')
        context = {'form': form, 'active_tab': 'personal'}
        return render(request, "teacher/personal_form.html", context)
