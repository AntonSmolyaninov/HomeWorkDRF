from rest_framework.pagination import PageNumberPagination


class CoursePagination(PageNumberPagination):
    """
    Пагинатор для списка курсов.
    """

    page_size = 5


class LessonPagination(PageNumberPagination):
    """
    Пагинатор для списка уроков.
    """

    page_size = 10
