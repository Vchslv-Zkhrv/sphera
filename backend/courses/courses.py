import os as _os

import aiofiles as _aiofiles
import fastapi as _fastapi


"""
Оперирует медиа-данными, относящимися к курсам

"""


def is_course_initialized(id: int):
    return _os.path.isdir(f"{_os.getcwd()}/courses/courses/{id}")


def initialize_course(id: int):
    if is_course_initialized(id):
        raise _fastapi.HTTPException(409, "Course already initialized")
    _os.mkdir(f"{_os.getcwd()}/courses/courses/{id}")


def is_lesson_initialized(course_id: int, lesson_number: int):
    return _os.path.isdir(f"{_os.getcwd()}/courses/courses/{course_id}/{lesson_number}")


def get_course_initialized_lessons(course_id: int):
    return list(map(int, _os.listdir(f"{_os.getcwd()}/courses/courses/{course_id}")))


def initialize_lesson(course_id: int, lesson_number: int):
    if is_lesson_initialized(course_id, lesson_number):
        raise _fastapi.HTTPException(409, "Course already initialized")
    _os.mkdir(f"{_os.getcwd()}/courses/courses/{course_id}/{lesson_number}")


def is_step_initialized(course_id: int, lesson_number: int, step_number: int):
    return _os.path.isfile(f"{_os.getcwd()}/courses/courses/{course_id}/{lesson_number}/{step_number}.txt")


def get_lesson_steps_numbers(course_id: int, lesson_number: int):
    return list(map(
        lambda step: int(step.split(".")[0]),
        _os.listdir(f"{_os.getcwd()}/courses/courses/{course_id}/{lesson_number}")
    ))


async def initialize_step(course_id: int, lesson_number: int):
    existing_steps = get_lesson_steps_numbers(course_id, lesson_number)
    step_number = 1 if not existing_steps else max(existing_steps)+1
    async with _aiofiles.open(
        f"{_os.getcwd()}/courses/courses/{course_id}/{lesson_number}/{step_number}.txt",
        "w",
        encoding="utf-8"
    ) as file:
        await file.write("")
    return step_number


async def get_step_text(course_id: int, lesson_number: int, step_number: int):
    if not is_step_initialized(course_id, lesson_number, step_number):
        raise _fastapi.HTTPException(404, "No such step in lesson")
    async with _aiofiles.open(
            f"{_os.getcwd()}/courses/courses/{course_id}/{lesson_number}/{step_number}.txt",
            "r",
            encoding="utf-8"
    ) as file:
        return await file.read()


def _find_step_image_name(course_id: int, lesson_number: int, step_number: int):
    steps = tuple(
        set(_os.listdir(f"{_os.getcwd()}/courses/courses/{course_id}/{lesson_number}"))
        .intersection({f"{step_number}.png", f"{step_number}.jpg", f"{step_number}.jpeg"})
    )
    assert len(steps) < 2
    return steps[0] if steps else None


def is_step_has_image(course_id: int, lesson_number: int, step_number: int):
    if not is_step_initialized(course_id, lesson_number, step_number):
        raise _fastapi.HTTPExceptio(404, "No such step in lesson")
    return bool(_find_step_image_name(course_id, lesson_number, step_number))


async def get_step_image(course_id: int, lesson_number: int, step_number: int):
    if not is_step_has_image(course_id, lesson_number, step_number):
        raise _fastapi.HTTPException(404, "No step image")
    image_name = _find_step_image_name(course_id, lesson_number, step_number)
    return _fastapi.responses.FileResponse(f"{_os.getcwd()}/courses/courses/{course_id}/{lesson_number}/{image_name}")


async def write_into_step(
        course_id: int,
        lesson_number: int,
        step_number: int,
        text: str
):
    if not is_step_initialized(course_id, lesson_number, step_number):
        raise _fastapi.HTTPException(404, "No such lesson step")
    async with _aiofiles.open(
            f"{_os.getcwd()}/courses/courses/{course_id}/{lesson_number}/{step_number}.txt",
            "w",
            encoding="utf-8"
    ) as file:
        await file.write(text)


async def upload_step_image(
        course_id: int,
        lesson_number: int,
        step_number: int,
        upload: _fastapi.UploadFile
):
    if not is_step_initialized(course_id, lesson_number, step_number):
        raise _fastapi.HTTPException(404, "No such lesson step")
    if is_step_has_image(course_id, lesson_number, step_number):
        raise _fastapi.HTTPException(409, "step already have an image")
    ext = upload.filename.split(".")[-1].lower()
    if ext not in ("png", "jpg", "jpeg"):
        raise _fastapi.HTTPException(415, "Unsupportable image type")
    if upload.size > 1048576:
        raise _fastapi.HTTPException(413, "Image too large")
    async with _aiofiles.open(
        f"{_os.getcwd()}/courses/courses/{course_id}/{lesson_number}/{step_number}.{ext}",
        "wb"
    ) as file:
        content = await upload.read()
        await file.write(content)


async def drop_step_image(
        course_id: int,
        lesson_number: int,
        step_number: int,
):
    if not is_step_initialized(course_id, lesson_number, step_number):
        raise _fastapi.HTTPException(404, "No such lesson step")
    if not is_step_has_image(course_id, lesson_number, step_number):
        raise _fastapi.HTTPException(404, "No image attached to step")
    image_name = _find_step_image_name(course_id, lesson_number, step_number)
    _os.remove(f"{_os.getcwd()}/courses/courses/{course_id}/{lesson_number}/{image_name}")
