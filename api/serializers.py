from rest_framework import serializers
from . import models
from django.db.models import Sum


class SponsorCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Sponsor
        fields = (
            'id',
            'full_name',
            'phone_number',
            'organization_name',
            'amount',
            'type',
        )

        extra_kwargs = {
            "id" : {
                "read_only": True
            }
        }

    def validate(self, attr):
        type = attr.get("type")
        org_name = attr.get("organization_name")

        # type == "physical"
        # a
        if type == "physical" and org_name:
            raise serializers.ValidationError(detail={
                "error": "Jismoniy shaxs tashkilot nomiga ega emas"
            })

        if type == "legal" and not org_name:
            raise serializers.ValidationError(detail={
                "error": "Yuridik shaxs tashkilot nomiga ega bo'lishi shart"
            })

        return  attr

class SponsorListSerializer(serializers.ModelSerializer):
    sponsor_amount = serializers.SerializerMethodField()

    def get_sponsor_amount(self, obj):
        a = obj.student_sponsors.aggregate(Sum('amount'))
        return a['amount__sum'] if a['amount__sum'] else 0

    class Meta:
        model = models.Sponsor
        fields = (
            'id',
            "full_name",
            "phone_number",
            "amount",
            "created_at",
            "status",
            "sponsor_amount",
        )


class SponsorUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Sponsor
        fields = "__all__"


class SponsorStudentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.StudentSponsor
        fields = "__all__"

    def create(self, validated_data):
        amount = validated_data.get('amount')
        student = validated_data.get("student")
        sponsor = validated_data.get("sponsor")

        # talabaga ajratiladigan pul miqdori oshib ketmasligi

        total_amount = sum(models.StudentSponsor.objects.filter(student=student).values_list("amount", flat=True))

        if total_amount + amount > student.contract:
            raise serializers.ValidationError(detail={
                "error": f"Siz ko'pi bilan {student.contract - total_amount} pul qo'sha olasiz "
            })

        return  super().create(validated_data)


class StudentListSerializer(serializers.ModelSerializer):
    student_amount = serializers.SerializerMethodField(method_name="total_student_amount")

    def total_student_amount(self, obj):
        result = sum(models.StudentSponsor.objects.filter(student=obj).values_list('amount', flat=True))
        return result

    class Meta:
        model = models.Student
        fields = ("id",
                  "full_name",
                  "contract",
                  "degree",
                  "university",
                  'student_amount'
                  )



