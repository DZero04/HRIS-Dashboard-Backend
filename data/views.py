from django.shortcuts import render
from rest_framework import viewsets, permissions
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Avg, Count, Q
from datetime import datetime
import ast
from collections import Counter
import re  # for regex splitting
import calendar
from collections import defaultdict
from calendar import monthrange
from django.utils.html import strip_tags
from django.db.models.functions import ExtractMonth




class DataTab1ToTab3Viewset(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = DataTab1ToTab3.objects.all()
    serializer_class = DataTab1ToTab3Serializer

    def list(self, request):
        queryset = DataTab1ToTab3.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

class DataTab4Viewset(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = DataTab4.objects.all()
    serializer_class = DataTab4Serializer

    def list(self, request):
        queryset = DataTab4.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class DataTab5OTViewset(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = DataTab5OT.objects.all()
    serializer_class = DataTab5OTSerializer

    def list(self, request):
        queryset = DataTab5OT.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

class DataTab5TravelViewset(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = DataTab5Travel.objects.all()
    serializer_class = DataTab5TravelSerializer

    def list(self, request):
        queryset = DataTab5Travel.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

class DataTab6Viewset(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = DataTab6.objects.all()
    serializer_class = DataTab6Serializer

    def list(self, request):
        queryset = DataTab6.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

class DataTab8Viewset(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = DataTab8.objects.all()
    serializer_class = DataTab8Serializer

    def list(self, request):
        queryset = DataTab8.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

class DataTab9Viewset(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = DataTab9.objects.all()
    serializer_class = DataTab9Serializer

    def list(self, request):
        queryset = DataTab9.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    
class DataChurnRiskViewset(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = DataChurnRisk.objects.all()
    serializer_class = DataChurnRiskSerializer

    def list(self, request):
        queryset = DataChurnRisk.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

class DataTab7Viewset(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = DataTab7.objects.all()
    serializer_class = DataTab7Serializer

    def list(self, request):
        queryset = DataTab7.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

# data for overview
class OverviewMetricsView(APIView):
    def get(self, request):
        offices = list(
            DataTab1ToTab3.objects
            .filter(office_alias__isnull=False)
            .exclude(office_alias__iexact='nan')
            .exclude(office_alias='')
            .values_list('office_alias', flat=True)
            .distinct()
        )

        data = {}

        def compute_metrics(active_qs, separated_qs):
            total_active = active_qs.count()
            total_separated = separated_qs.count()
            total_employees = total_active + total_separated

            avg_tenure = round(active_qs.aggregate(avg=Avg('tenure_years'))['avg'] or 0, 2)
            recent_hires = active_qs.filter(date_hire__year__gte=2024).count()
            turnover = separated_qs.filter(
                effective_date__year__gte=2024
            ).count()

            turnover_rate = f"{round((turnover / total_active) * 100, 2) if total_active > 0 else 0}%"

            # Pie chart data (only for active employees)
            status_counts = active_qs.values('employment_status').annotate(count=Count('id'))
            pie_data = []
            for s in ['PERMANENT', 'CONTRACTUAL']:
                count = next((item['count'] for item in status_counts if item['employment_status'] == s), 0)
                pie_data.append({"name": s.capitalize(), "value": count})

            # Line chart data: active employees per year
             # Line chart: Cumulative active employee simulation
            line_data = []
            years = list(range(2015, 2026))

            # Initial base: hired before 2015
            emp_count = active_qs.filter(date_hire__year__lt=2015).count() + separated_qs.filter(date_hire__year__lt=2015).count()
            

            for year in years:
                hired_this_year = active_qs.filter(date_hire__year=year).count() + separated_qs.filter(date_hire__year=year).count()
                separated_this_year = separated_qs.filter(effective_date__year=year).count()

                emp_count += hired_this_year
                emp_count -= separated_this_year

                line_data.append({"name": str(year), "value": emp_count})

            return {
                "metrics": {
                    "total_employees": total_active,
                    "average_tenure": avg_tenure,
                    "recent_hires": recent_hires,
                    "turnover_rate": turnover_rate,
                },
                "pieData": pie_data,
                "lineData": line_data
            }

        # Compute for All Offices
        active_all = DataTab1ToTab3.objects.filter(
            status=1,
            employment_status__in=['PERMANENT', 'CONTRACTUAL']
        )
        separated_all = DataTab1ToTab3.objects.filter(status=0)
        data['All Offices'] = compute_metrics(active_all, separated_all)

        # Compute for each office
        for office in offices:
            active_office = DataTab1ToTab3.objects.filter(
                office_alias=office,
                status=1,
                employment_status__in=['PERMANENT', 'CONTRACTUAL']
            )
            separated_office = DataTab1ToTab3.objects.filter(
                office_alias=office,
                status=0
            )
            data[office] = compute_metrics(active_office, separated_office)

        return Response(data)
    
# data for workforce body
class EmployeeCompositionView(APIView):
    def get(self, request):
        data = {}
        offices = list(
            DataTab1ToTab3.objects
            .filter(office_alias__isnull=False)
            .exclude(office_alias__iexact='nan')  # Exclude string 'nan' (case-insensitive)
            .exclude(office_alias='')             # Also exclude empty strings, just in case
            .values_list('office_alias', flat=True)
            .distinct()
        )

        def compute_composition(qs):
            # Gender distribution
            gender_map = {0: 'Female', 1: 'Male'}
            gender_counts = qs.values('sex').annotate(count=Count('id'))
            genderData = [
                {"name": gender_map.get(item['sex'], 'Other'), "value": item['count']}
                for item in gender_counts
            ]

            # Civil status distribution
            civil_map = {0: 'Single', 1: 'Married', 2: 'Widowed', 3: 'Separated'}
            civil_counts = qs.values('civil_status').annotate(count=Count('id'))
            civilStatusData = [
                {"name": civil_map.get(item['civil_status'], 'Other'), "value": item['count']}
                for item in civil_counts
            ]

            # Diversity
            diversityData = [
                {"name": "IP", "value": qs.filter(ip=1).count()},
                {"name": "PWD", "value": qs.filter(pwd=1).count()},
                {"name": "Solo Parent", "value": qs.filter(solo_parent=1).count()},
            ]

            # Tenure
            def get_tenure_bracket(years):
                if years is None: return None
                if years < 5: return '0-4'
                elif years < 10: return '5-9'
                elif years < 15: return '10-14'
                elif years < 20: return '15-19'
                elif years < 25: return '20-24'
                elif years < 30: return '25-29'
                elif years < 35: return '30-34'
                elif years < 40: return '35-39'
                elif years < 45: return '40-44'
                elif years < 50: return '45-49'
                else: return '50+'

            tenure_brackets = Counter(get_tenure_bracket(emp.tenure_years) for emp in qs)
            # tenureData = [{"year": k, "value": v} for k, v in sorted(tenure_brackets.items()) if k is not None]
            # Defined logical order for display
            tenure_order = ['0-4', '5-9', '10-14', '15-19', '20-24', '25-29',
                            '30-34', '35-39', '40-44', '45-49', '50+']

            tenureData = [{"year": bracket, "value": tenure_brackets.get(bracket, 0)} for bracket in tenure_order]

            # Age
            def get_age_bracket(age):
                if age is None: return None
                if age < 25: return '20-24'
                elif age < 30: return '25-29'
                elif age < 35: return '30-34'
                elif age < 40: return '35-39'
                elif age < 45: return '40-44'
                elif age < 50: return '44-49'
                else: return '50+'

            age_brackets = Counter(get_age_bracket(emp.age) for emp in qs)
            # ageData = [{"age": k, "value": v} for k, v in sorted(age_brackets.items()) if k is not None]

            age_order = ['20-24', '25-29', '30-34', '35-39', '40-44', '44-49', '50+']
            ageData = [{"age": bracket, "value": age_brackets.get(bracket, 0)} for bracket in age_order]


            # Job levels
            job_level_counts = qs.values('job_level').annotate(count=Count('id'))
            jobLevelData = [{"level": item['job_level'], "value": item['count']} for item in job_level_counts]

            # Skills word frequency (case-insensitive, split on space and slash)
            all_skill_words = []

            for emp in qs:
                if emp.skills:
                    try:
                        parsed = ast.literal_eval(emp.skills)
                        for skill in parsed:
                            if isinstance(skill, str):
                                # Normalize: lowercase, strip, and split on space or slash
                                words = re.split(r'[\s/]+', skill.strip().lower())
                                all_skill_words.extend(words)
                    except:
                        continue

            # Count frequency and title-case for display
            skill_counts = Counter(all_skill_words)
            skills = [{"text": word.title(), "value": count} for word, count in skill_counts.items() if word]

            return {
                "genderData": genderData,
                "civilStatusData": civilStatusData,
                "diversityData": diversityData,
                "tenureData": tenureData,
                "ageData": ageData,
                "jobLevelData": jobLevelData,
                "skills": skills,
            }
        
        # All offices
        all_qs = DataTab1ToTab3.objects.filter(
            status=1,
            employment_status__in=['PERMANENT', 'CONTRACTUAL']
        )
        data["All Offices"] = compute_composition(all_qs)

        # Per office
        for office in offices:
            office_qs = DataTab1ToTab3.objects.filter(
                office_alias=office,
                status=1,
                employment_status__in=['PERMANENT', 'CONTRACTUAL']
            )
            data[office] = compute_composition(office_qs)

        return Response(data)
    

# workforce turnover
class SeparatedEmployeeAnalyticsView(APIView):
    def get(self, request):
        data = {}

        # Get all distinct office_alias values
        offices = DataTab1ToTab3.objects \
            .exclude(office_alias__isnull=True) \
            .exclude(office_alias__exact='') \
            .exclude(office_alias__iexact='nan') \
            .values_list('office_alias', flat=True) \
            .distinct()

        # Get all years with separation data
        year_values = DataTab1ToTab3.objects.filter(status=0, effective_date__isnull=False) \
            .dates('effective_date', 'year')
        years = sorted([str(y.year) for y in year_values])

        # Add 'All Offices'
        offices = ['All Offices'] + list(offices)

        # Month name map
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                       'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        gender_map = {1: 'Male', 0: 'Female'}

        for office in offices:
            data[office] = {}

            # Filter base querysets
            active_qs = DataTab1ToTab3.objects.filter(status=1)
            separated_qs = DataTab1ToTab3.objects.filter(status=0)

            if office != 'All Offices':
                active_qs = active_qs.filter(office_alias=office)
                separated_qs = separated_qs.filter(office_alias=office)

            # Per Year Data
            for year in years:
                year_int = int(year)
                year_sep_qs = separated_qs.filter(effective_date__year=year_int)

                total_separated = year_sep_qs.count()
                avg_tenure = round(year_sep_qs.aggregate(avg=Avg('tenure_years'))['avg'] or 0, 2)

                # Age Group
                def get_age_bracket(age):
                    if age is None:
                        return None
                    if age < 25:
                        return '20-24'
                    elif age < 30:
                        return '25-29'
                    elif age < 35:
                        return '30-34'
                    elif age < 40:
                        return '35-39'
                    elif age < 45:
                        return '40-44'
                    elif age < 50:
                        return '45-49'
                    else:
                        return '50+'

                # Apply to age values in queryset
                age_brackets = [
                    get_age_bracket(obj.age)
                    for obj in year_sep_qs.only('age')
                    if get_age_bracket(obj.age) is not None
                ]
                age_counts = Counter(age_brackets)
                age_group_data = [{"age": age, "value": count} for age, count in sorted(age_counts.items())]

                # Gender
                gender_counts = year_sep_qs.values('sex').annotate(value=Count('id'))
                gender_data = [{"name": gender_map.get(item['sex'], 'Other'), "value": item['value']} for item in gender_counts]

                # Hiring vs Separation Over Time
                hiring_sep_data = []
                for y in range(2017, 2026):  # Update range as needed
                    hires = active_qs.filter(date_hire__year=y).count()
                    seps = separated_qs.filter(effective_date__year=y).count()
                    hiring_sep_data.append({
                        "year": str(y),
                        "hiring": hires,
                        "separation": seps
                    })

                # Monthly Separation
                month_qs = year_sep_qs.annotate(month=ExtractMonth('effective_date')) \
                      .values('month') \
                      .annotate(value=Count('id')) \
                      .order_by('month')
                month_data = [
                    {"month": month_names[int(item['month']) - 1], "value": item['value']}
                    for item in month_qs
                ]

                data[office][year] = {
                    "separated": total_separated,
                    "tenure": avg_tenure,
                    "ageGroup": age_group_data,
                    "gender": gender_data,
                    "hiringSeparation": hiring_sep_data,
                    "monthSeparation": month_data
                }

            # "All" Year Aggregation
            total_separated_all = separated_qs.count()
            avg_tenure_all = round(separated_qs.aggregate(avg=Avg('tenure_years'))['avg'] or 0, 2)

            age_brackets_all = [
                get_age_bracket(obj.age)
                for obj in separated_qs.only('age')
                if get_age_bracket(obj.age) is not None
            ]
            age_counts_all = Counter(age_brackets_all)
            age_group_data_all = [{"age": age, "value": count} for age, count in sorted(age_counts_all.items())]

            age_order = ['20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50+']
            age_group_data = [{"age": age, "value": age_counts.get(age, 0)} for age in age_order if age_counts.get(age)]

            gender_counts_all = separated_qs.values('sex').annotate(value=Count('id'))
            gender_data_all = [{"name": gender_map.get(item['sex'], 'Other'), "value": item['value']} for item in gender_counts_all]

            hiring_sep_data_all = []
            for y in range(2018, 2023):
                hires = active_qs.filter(date_hire__year=y).count()
                seps = separated_qs.filter(effective_date__year=y).count()
                hiring_sep_data_all.append({
                    "year": str(y),
                    "hiring": hires,
                    "separation": seps
                })
            
         
            month_qs_all = separated_qs.annotate(month=ExtractMonth('effective_date')) \
                .values('month') \
                .annotate(value=Count('id')) \
                .order_by('month')
            month_data_all = [
                {"month": month_names[int(item['month']) - 1], "value": item['value']}
                for item in month_qs_all
            ]

            data[office]["All"] = {
                "separated": total_separated_all,
                "tenure": avg_tenure_all,
                "ageGroup": age_group_data_all,
                "gender": gender_data_all,
                "hiringSeparation": hiring_sep_data_all,
                "monthSeparation": month_data_all
            }

        return Response(data)



# leave administration
class LeaveAnalyticsView(APIView):
    def get(self, request):
        office_filter = request.query_params.get('office_alias', None)
        year_filter = request.query_params.get('year', None)

        all_qs = DataTab4.objects.all()
        offices = all_qs.values_list('office_alias', flat=True).distinct()
        years = all_qs.dates('from_date', 'year')

        data = {}

        def compute_group(qs):
            leaveDays = round(qs.aggregate(avg=Avg('days_leave'))['avg'] or 0, 1)

            def get_age_bracket(age):
                if age is None:
                    return None
                if age < 25:
                    return '20-24'
                elif age < 30:
                    return '25-29'
                elif age < 35:
                    return '30-34'
                elif age < 40:
                    return '35-39'
                elif age < 45:
                    return '40-44'
                elif age < 50:
                    return '44-49'
                else:
                    return '50+'

            age_brackets = Counter(get_age_bracket(emp.age) for emp in qs if emp.age is not None)
            age_order = ['20-24', '25-29', '30-34', '35-39', '40-44', '44-49', '50+']
            ageData = [{"age": bracket, "value": age_brackets.get(bracket, 0)} for bracket in age_order]

            gender_map = {0: 'Female', 1: 'Male'}
            gender_counts = Counter(gender_map.get(emp.sex, 'Other') for emp in qs if emp.sex in [0, 1])
            gender = [{"name": k, "value": v} for k, v in gender_counts.items()]

            month_counts = Counter(emp.from_date.month for emp in qs if emp.from_date)
            leaveMonthly = [{"month": calendar.month_abbr[m], "value": month_counts.get(m, 0)} for m in range(1, 13)]

            leave_type_counts = Counter(emp.type.strip() for emp in qs if emp.type and emp.type.strip().lower() != "nan")
            leaveType = [{"type": k, "value": v} for k, v in sorted(leave_type_counts.items())]

            purpose_counts = Counter()
            for emp in qs:
                if emp.vl_reason and emp.vl_reason.lower() != "nan":
                    purpose = emp.vl_reason.strip().lower().title()
                    purpose_counts[purpose] += 1
            leavePurpose = [{"text": k, "value": v} for k, v in purpose_counts.items()]

            return {
                "leaveDays": leaveDays,
                "ageData": ageData,
                "gender": gender,
                "leaveMonthly": leaveMonthly,
                "leaveType": leaveType,
                "leavePurpose": leavePurpose
            }

        # Loop through each office (including "All Offices")
        for office in list(offices) + ["All Offices"]:
            office_data = {}

            for year in years:
                year_int = year.year
                qs = all_qs.filter(from_date__year=year_int)
                if office != "All Offices":
                    qs = qs.filter(office_alias=office)

                if not qs.exists():
                    continue

                if office_filter and office_filter != office:
                    continue
                if year_filter and str(year_int) != str(year_filter):
                    continue

                office_data[str(year_int)] = compute_group(qs)

            # Add data for all years combined
            qs_all_years = all_qs
            if office != "All Offices":
                qs_all_years = qs_all_years.filter(office_alias=office)
            if not year_filter and (not office_filter or office_filter == office):
                if qs_all_years.exists():
                    office_data["All Years"] = compute_group(qs_all_years)

            if office_data:
                data[office] = office_data

        return Response(data)


class OvertimeTravelAnalyticsView(APIView):
    def get(self, request):
        result = defaultdict(lambda: defaultdict(lambda: {
            'overtime': defaultdict(lambda: defaultdict(lambda: [0]*12)),
            'travel': defaultdict(lambda: defaultdict(lambda: [0]*12)),
            'overtimePurpose': defaultdict(int),
            'travelDestination': defaultdict(int),
            'travelDuration': {'0-2': 0, '2-4': 0, '4-6': 0, '6+': 0}
        }))

        # -------------------------
        # Process Overtime Records
        # -------------------------
        for rec in DataTab5OT.objects.all():
            year = rec.date_start.year
            month = rec.date_start.month - 1  # index 0–11
            office = rec.office_alias or "Unknown"
            level = rec.job_level or "Unknown"
            emp = rec.empId or "Unknown"
            purpose_text = strip_tags(rec.purpose)[:50]  # strip HTML, trim

            result[str(year)][office]['overtime'][level][emp][month] += 1
            result[str(year)][office]['overtimePurpose'][purpose_text] += 1

        # -------------------------
        # Process Travel Records
        # -------------------------
        for rec in DataTab5Travel.objects.all():
            year = rec.date_from.year
            month = rec.date_from.month - 1
            office = rec.office_alias or "Unknown"
            level = rec.job_level or "Unknown"
            emp = rec.empId or "Unknown"
            purpose_text = rec.purpose[:50]
            destination = rec.destintion or "Unknown"
            duration = rec.travel_durations or 0

            result[str(year)][office]['travel'][level][emp][month] += 1
            result[str(year)][office]['travelDestination'][destination] += 1

            if duration <= 2:
                result[str(year)][office]['travelDuration']['0-2'] += 1
            elif duration <= 4:
                result[str(year)][office]['travelDuration']['2-4'] += 1
            elif duration <= 6:
                result[str(year)][office]['travelDuration']['4-6'] += 1
            else:
                result[str(year)][office]['travelDuration']['6+'] += 1


        # -------------------------
        # Convert defaultdicts to normal dicts
        # -------------------------
        final_result = {}
        for year, offices in result.items():
            final_result[year] = {}
            for office, data in offices.items():
                final_result[year][office] = {
                    'overtime': {lvl: dict(emp) for lvl, emp in data['overtime'].items()},
                    'travel': {lvl: dict(emp) for lvl, emp in data['travel'].items()},
                    'overtimePurpose': [{'text': k, 'value': v} for k, v in data['overtimePurpose'].items()],
                    'travelDestination': [{'text': k, 'value': v} for k, v in data['travelDestination'].items()],
                    'travelDuration': [{'name': k, 'value': v} for k, v in data['travelDuration'].items()],
                }

        return Response(final_result)


# request form tab
class RequestSummaryView(APIView):
    def get(self, request):
        data = defaultdict(lambda: {
            "totalRequests": 0,
            "overTime": [],
            "purposeWords": [],
            "mostRequested": []
        })

        qs = DataTab6.objects.all()
        all_offices = set()
        year_counter_all = Counter()
        purpose_counter_all = Counter()
        form_counter_all = Counter()

        office_map = defaultdict(list)

        for entry in qs:
            office = entry.office_alias or "Unknown"
            all_offices.add(office)
            year = entry.created_at.year
            data[office]["totalRequests"] += 1
            year_counter = Counter()
            purpose_counter = Counter()
            form_counter = Counter()

            office_map[office].append(entry)

            # Count for "All Offices"
            year_counter_all[year] += 1
            purpose_counter_all[entry.purpose.strip()] += 1
            form_counter_all[entry.selected_form_text.strip()] += 1

        # Process office-specific
        for office, entries in office_map.items():
            year_counter = Counter()
            purpose_counter = Counter()
            form_counter = Counter()

            for e in entries:
                year_counter[e.created_at.year] += 1
                purpose_counter[e.purpose.strip()] += 1
                form_counter[e.selected_form_text.strip()] += 1

            data[office]["overTime"] = [{"year": y, "value": v} for y, v in sorted(year_counter.items())]
            data[office]["purposeWords"] = [{"text": k, "value": v} for k, v in purpose_counter.most_common(10)]
            data[office]["mostRequested"] = [{"name": k, "value": v} for k, v in form_counter.most_common(10)]

        # Add "All Offices"
        data["All Offices"]["totalRequests"] = qs.count()
        data["All Offices"]["overTime"] = [{"year": y, "value": v} for y, v in sorted(year_counter_all.items())]
        data["All Offices"]["purposeWords"] = [{"text": k, "value": v} for k, v in purpose_counter_all.most_common(10)]
        data["All Offices"]["mostRequested"] = [{"name": k, "value": v} for k, v in form_counter_all.most_common(10)]

        return Response(data)
    
# learning and development
class TrainingAnalyticsView(APIView):
    def get(self, request):
        qs = DataTab8.objects.all()
        offices = qs.values_list('office_alias', flat=True).distinct()

        result = {}

        def compute_office_data(qs_filtered):
            # Total Trainings
            total_trainings = qs_filtered.count()

            # Total Employees (distinct empId)
            total_employees = qs_filtered.values('empId').distinct().count()

            # Training Trend (by year)
            trend = defaultdict(int)
            for entry in qs_filtered:
                if entry.converted_date:
                    year = entry.converted_date.year
                    trend[year] += 1
            training_trend = [{"year": str(k), "value": v} for k, v in sorted(trend.items())]

            # Training Types
            type_counts = qs_filtered.values('type').annotate(count=Count('type'))
            training_types = [{"name": item['type'], "value": item['count']} for item in type_counts]

            # Training Split (Local vs. International)
            normalized_split = defaultdict(int)
            for entry in qs_filtered:
                if entry.international:
                    key = entry.international.strip().title()
                    normalized_split[key] += 1

            total_split = sum(normalized_split.values())
            training_split = [
                {
                    "name": name,
                    "value": round((count / total_split) * 100, 1) if total_split else 0
                }
                for name, count in normalized_split.items()
            ]

            return {
                "totalTrainings": total_trainings,
                "totalEmployees": total_employees,
                "trainingTrend": training_trend,
                "trainingTypes": training_types,
                "trainingSplit": training_split
            }

        # Per office
        for office in offices:
            office_qs = qs.filter(office_alias=office)
            result[office] = compute_office_data(office_qs)

        # All Offices combined
        result["All Offices"] = compute_office_data(qs)

        return Response(result)
    

# aspirations
class TalentDevelopmentView(APIView):
    def get(self, request):
        qs = DataTab9.objects.all()
        offices = qs.values_list('office_alias', flat=True).distinct()
        data = {}

        for office in ['All Offices'] + list(offices):
            office_qs = qs if office == 'All Offices' else qs.filter(office_alias=office)
            
            # Competencies
            comp_counter = Counter()
            for entry in office_qs:
                if entry.competencies:
                    for word in entry.competencies.lower().split(","):
                        comp_counter[word.strip()] += 1
            competencies = [{"text": k, "value": v * 10} for k, v in comp_counter.items()]

            # Desired Positions
            position_counter = Counter(entry.position for entry in office_qs if entry.position)
            desired_positions = [{"name": pos, "size": count * 10} for pos, count in position_counter.items()]

            # Status by Office
            status_counter = defaultdict(lambda: {"Permanent": 0, "Contractual": 0})
            for entry in office_qs:
                status_counter[entry.office_alias][entry.employment_status.capitalize()] += 1
            status_by_office = [{"name": k, **v} for k, v in status_counter.items()]

            # Aspirations
            asp_counter = defaultdict(lambda: {"Short": 0, "Medium": 0, "Long": 0})
            for entry in office_qs:
                aspiration = entry.position.split(" ")[0] if entry.position else "General"
                term = entry.term.capitalize() if entry.term else "Short"
                asp_counter[aspiration][term] += 1
            aspirations = [{"name": k, **v} for k, v in asp_counter.items()]

            # Target Offices
            target_counter = Counter(entry.target_office for entry in office_qs if entry.target_office)
            target_offices = [{"name": k, "value": v} for k, v in target_counter.items()]

            data[office] = {
                "competencies": competencies,
                "desiredPositions": desired_positions,
                "statusByOffice": status_by_office,
                "aspirations": aspirations,
                "targetOffices": target_offices
            }

        return Response(data)
    


class RiskScoreView(APIView):
    def get(self, request):
        # Get all records
        qs = DataChurnRisk.objects.all()

        # Initialize data structure
        data = {}
        all_offices_data = []

        for emp in qs:
            emp_data = {
                "Employee": emp.empId,
                "Office": emp.office_alias,
                "Tenure": round(float(emp.tenure_years), 2) if emp.tenure_years else 0,
                "RiskScore": emp.risk_score,
                "RiskLevel": emp.risk_level
            }

            # Add to "All Offices"
            all_offices_data.append(emp_data)

            # Group by office_alias
            office = emp.office_alias
            if office not in data:
                data[office] = []
            data[office].append(emp_data)

        # Add "All Offices" key
        data["All Offices"] = all_offices_data

        return Response(data)



class HiringAnalyticsView(APIView):
    def get(self, request):
        def get_age_bracket(age):
            if age is None:
                return None
            if age < 25:
                return '20-24'
            elif age < 30:
                return '25-29'
            elif age < 35:
                return '30-34'
            elif age < 40:
                return '35-39'
            elif age < 45:
                return '40-44'
            elif age < 50:
                return '45-49'
            else:
                return '50+'

        data = defaultdict(lambda: defaultdict(dict))
        raw_qs = DataTab7.objects.all()

        for row in raw_qs:
            pub = row.publication_title
            pos = row.position
            applicant_type = 'external' if row.type.lower() == 'outsider' else 'internal'
            item = data[pub][pos]

            # Initialize if not already
            item.setdefault('external', 0)
            item.setdefault('internal', 0)
            item.setdefault('age_sum', 0)
            item.setdefault('age_count', 0)
            item.setdefault('age_bracket_counter', Counter())
            item.setdefault('gender_counter', Counter())
            item.setdefault('civil_counter', Counter())
            item.setdefault('education_counter', Counter())
            item.setdefault('career_counter', Counter())
            item.setdefault('success', {
                'external': [
                    {"name": "1st Eval", "value": 0},
                    {"name": "2nd Eval", "value": 0},
                    {"name": "Final", "value": 0}
                ],
                'internal': [
                    {"name": "1st Eval", "value": 0},
                    {"name": "2nd Eval", "value": 0},
                    {"name": "Final", "value": 0}
                ]
            })

            # Basic counts
            item[applicant_type] += 1

            # Age processing
            if row.age:
                item['age_sum'] += row.age
                item['age_count'] += 1
                bracket = get_age_bracket(row.age)
                if bracket:
                    item['age_bracket_counter'][bracket] += 1

            # Gender and civil
            item['gender_counter'][row.sex] += 1
            item['civil_counter'][row.civil_status] += 1

            # Education
            try:
                levels = ast.literal_eval(row.level)
                item['education_counter'].update(levels)
            except:
                pass

            # Career
            try:
                careers = ast.literal_eval(row.career)
                item['career_counter'].update(careers)
            except:
                pass

            # Success steps (funnel chart data)
            if row.first == 1:
                item['success'][applicant_type][0]['value'] += 1
            if row.second == 1:
                item['success'][applicant_type][1]['value'] += 1
            if row.hired == 1:
                item['success'][applicant_type][2]['value'] += 1

        # Final structure for frontend
        final = {}
        for pub, positions in data.items():
            final[pub] = {}
            for pos, item in positions.items():
                age = round(item['age_sum'] / item['age_count'], 1) if item['age_count'] else 0

                gender = [{"name": 'Male' if k == 0 else 'Female', "value": v} for k, v in item['gender_counter'].items()]
                civil_map = {0: 'Single', 1: 'Married', 2: 'Widowed', 3: 'Separated'}
                civil = [{"name": civil_map.get(k, str(k)), "value": v} for k, v in item['civil_counter'].items()]
                education = [{"name": k.title(), "value": v} for k, v in item['education_counter'].items()]
                career = [{"text": k, "value": v} for k, v in item['career_counter'].items()]
                age_distribution = [{"name": k, "value": v} for k, v in sorted(item['age_bracket_counter'].items())]
                success = item['success']

                final[pub][pos] = {
                    "external": item['external'],
                    "internal": item['internal'],
                    "age": age,
                    "gender": gender,
                    "civil": civil,
                    "education": education,
                    "career": career,
                    "success": success,
                    "age_distribution": age_distribution
                }

        return Response(final)
