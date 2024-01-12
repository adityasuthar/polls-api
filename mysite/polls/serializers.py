from rest_framework import serializers
from .models import Question, Choice


class QuestionChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ("id", "choice_text")


class ChoiceSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(read_only=True)
    # choice_text = serializers.CharField(max_length=200)

    # def create(self, validated_data):
    #     return Choice.objects.create(**validated_data)

    class Meta:
        model = Choice
        fields = ("choice_text",)


class QuestionDetailPageSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)
    was_published_recently = serializers.BooleanField(read_only=True)
    choice_set = QuestionChoiceSerializer(read_only=True, many=True)

    class Meta:
        model = Question
        fields = "__all__"


class QuestionListPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"

    was_published_recently = serializers.BooleanField(read_only=True)


class QuestionDetailPageSerializer(QuestionListPageSerializer):
    choice_set = QuestionChoiceSerializer(read_only=True)

    def create(self, validated_data):
        choice_validated_data = validated_data.pop("choice_set")
        question = Question.objects.all(**validated_data)
        choice_set_serializer = self.fields("choice_set")
        for each in choice_validated_data:
            each["question"] = question
        choices = ChoiceSerializer.create(choice_validated_data)
        return question


class QuestionListPageSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    question_text = serializers.CharField(max_length=200)
    pub_date = serializers.DateTimeField()
    was_published_recently = serializers.BooleanField(read_only=True)
    # verbose_question_text = serializers.CharField(read_only=True)
    choices = ChoiceSerializer(many=True, write_only=True, required=False)

    def create(self, validated_data):
        choices = validated_data.pop("choices", [])
        question = Question.objects.create(**validated_data)
        for choice_dict in choices:
            choice_dict["question"] = question
            Choice.objects.create(**choice_dict)
        return question

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class QuestionDetailPageSerializer(QuestionListPageSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class MultipleQuestionsCreateSerializer(serializers.Serializer):
    questions = QuestionListPageSerializer(write_only=True)


class VoteSerializer(serializers.Serializer):
    choice_id = serializers.IntegerField()


class ChoiceSerializerWithVotes(ChoiceSerializer):
    votes = serializers.IntegerField(read_only=True)


class QuestionResultPageSerializer(QuestionListPageSerializer):
    choice = ChoiceSerializerWithVotes(many=True, read_only=True)
    max_voted_choice = ChoiceSerializerWithVotes(read_only=True)
