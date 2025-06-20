from django.db import models


class DataTab1ToTab3(models.Model):
    id_num = models.IntegerField()
    empId = models.CharField(max_length = 200)
    date_hire = models.DateField()
    dob = models.DateField()
    sex = models.IntegerField()
    civil_status = models.IntegerField()
    ip = models.IntegerField()
    pwd = models.IntegerField()
    solo_parent = models.IntegerField()
    status = models.IntegerField()
    effective_date = models.DateField()
    employment_status = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    office_alias = models.CharField(max_length=200)
    office_name = models.CharField(max_length=200)
    division_name = models.CharField(max_length=200)
    age = models.IntegerField()
    tenure_years = models.DecimalField(max_digits=10, decimal_places=2)
    sg = models.IntegerField()
    job_level = models.CharField(max_length=200)
    skills = models.CharField(max_length=500)

class DataTab4(models.Model):
    empId = models.IntegerField()
    leave_type = models.IntegerField()
    vl_reason = models.CharField(max_length=200)
    from_date = models.DateField()
    to_date = models.DateField()
    days_leave = models.IntegerField()
    status = models.IntegerField()
    sex = models.IntegerField()
    age = models.IntegerField()
    office_alias = models.CharField(max_length=200)
    office_name = models.CharField(max_length=200)
    division_name = models.CharField(max_length=200)
    type = models.CharField(max_length=200)

class DataTab5OT(models.Model):
    empId = models.CharField(max_length=200)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    purpose = models.CharField(max_length=1000)
    employment_status = models.CharField(max_length=200)
    office_alias = models.CharField(max_length=200)
    office_name = models.CharField(max_length=200)
    job_level = models.CharField(max_length=200)

class DataTab5Travel(models.Model):
    empId = models.CharField(max_length=200)
    date_from = models.DateField()
    date_to = models.DateField()
    purpose = models.CharField(max_length=1000)
    destintion = models.CharField(max_length= 200)
    employment_status = models.CharField(max_length=200)
    office_alias = models.CharField(max_length=200)
    office_name = models.CharField(max_length=200)
    job_level = models.CharField(max_length=200)
    travel_durations = models.IntegerField()

class DataTab6(models.Model):
    empId = models.CharField(max_length=200)
    selected_form_text = models.CharField(max_length=200)
    purpose = models.CharField(max_length=500)
    others = models.CharField(max_length=400)
    created_at = models.DateTimeField()
    employment_status = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    office_alias = models.CharField(max_length=200)
    office_name = models.CharField(max_length=200)
    job_level = models.CharField(max_length=200)

class DataTab8(models.Model):
    empId = models.CharField(max_length=200)
    converted_date = models.DateField()
    title = models.CharField(max_length=500)
    hours = models.IntegerField()
    type = models.CharField(max_length=200)
    international = models.CharField(max_length=200)
    employment_status = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    office_alias = models.CharField(max_length=200)
    job_level = models.CharField(max_length=200)


class DataTab9(models.Model):
    empId = models.CharField(max_length=200)
    term = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    target_office = models.CharField(max_length = 200)
    competencies = models.CharField(max_length=500)
    office_alias = models.CharField(max_length=200)
    employment_status = models.CharField(max_length=200)

class DataChurnRisk(models.Model):
    empId = models.CharField(max_length=200)
    office_alias = models.CharField(max_length=200)
    tenure_years = models.DecimalField(max_digits=10, decimal_places=2)
    risk_score = models.IntegerField()
    risk_level = models.CharField(max_length=200)

class DataTab7(models.Model):
    publication_position_id = models.IntegerField()
    user_id = models.IntegerField()
    type = models.CharField(max_length=200)
    first = models.IntegerField()
    second = models.IntegerField()
    hired = models.IntegerField()
    publication_title = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    sex = models.IntegerField()
    civil_status = models.IntegerField()
    level = models.CharField(max_length=200)
    career = models.CharField(max_length=500)
    age = models.IntegerField()  
    

    