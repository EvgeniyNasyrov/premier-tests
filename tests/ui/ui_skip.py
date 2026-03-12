def skip_reason_for_ui_exception(e: Exception, section_name: str | None = None, kind: str = "default") -> str | None:
    err = str(e)
    is_timeout = "Timeout" in type(e).__name__
    is_network = "ERR_CONNECTION_RESET" in err or "net::ERR_" in err

    if is_network:
        return f"Сетевая ошибка при загрузке premier.one: {e!s}"
    if kind == "login" and (
        "Войти" in err or "Unable to locate" in err or "auth" in err or "login" in err or is_timeout
    ):
        return "Кнопка входа не найдена (страница не загрузилась или изменилась вёрстка premier.one)"
    if kind == "section" and ("Unable to locate" in err or is_timeout):
        return (
            f"Раздел «{section_name}» не найден в меню (возможно, изменилась вёрстка premier.one)"
            if section_name
            else "Раздел не найден в меню"
        )
    if kind == "search" and ("Unable to locate" in err or "оиск" in err or "search" in err.lower() or is_timeout):
        return "Кнопка поиска или результаты не найдены (изменилась вёрстка premier.one)"
    if kind == "default" and (
        "Войти" in err or "Unable to locate" in err or "auth" in err or "login" in err or is_timeout
    ):
        return "Кнопка входа не найдена (страница не загрузилась или изменилась вёрстка premier.one)"
    return None
