# Модель ответа - Возвращаемый тип

Вы можете объявить тип ответа, указав аннотацию **возвращаемого значения** для *функции операции пути*.

FastAPI позволяет использовать **аннотации типов** таким же способом, как и для ввода данных в  **параметры** функции, вы можете использовать модели Pydantic, списки, словари, скалярные типы (такие, как int, bool и т.д.).

//// tab | Python 3.10+

```Python hl_lines="16  21"
{!> ../../docs_src/response_model/tutorial001_01_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="18  23"
{!> ../../docs_src/response_model/tutorial001_01_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="18  23"
{!> ../../docs_src/response_model/tutorial001_01.py!}
```

////

FastAPI будет использовать этот возвращаемый тип для:

* **Валидации** ответа.
  * Если данные невалидны (например, отсутствует одно из полей), это означает, что код *вашего* приложения работает некорректно и функция возвращает не то, что вы ожидаете. В таком случае приложение вернет server error вместо того, чтобы отправить неправильные данные. Таким образом, вы и ваши пользователи можете быть уверены, что получите корректные данные в том виде, в котором они ожидаются.
* Добавьте **JSON схему** для ответа внутри *операции пути* OpenAPI.
  * Она будет использована для **автоматически генерируемой документации**.
  * А также - для автоматической кодогенерации пользователями.

Но самое важное:

* Ответ будет **ограничен и отфильтрован** - т.е. в нем останутся только те данные, которые определены в возвращаемом типе.
  * Это особенно важно для **безопасности**, далее мы рассмотрим эту тему подробнее.

## Параметр `response_model`

Бывают случаи, когда вам необходимо (или просто хочется) возвращать данные, которые не полностью соответствуют объявленному типу.

Допустим, вы хотите, чтобы ваша функция **возвращала словарь (dict)** или объект из базы данных, но при этом **объявляете выходной тип как модель Pydantic**. Тогда именно указанная модель будет использована для автоматической документации, валидации и т.п. для объекта, который вы вернули (например, словаря или объекта из базы данных).

Но если указать аннотацию возвращаемого типа, статическая проверка типов будет выдавать ошибку (абсолютно корректную в данном случае). Она будет говорить о том, что ваша функция должна возвращать данные одного типа (например, dict), а в аннотации вы объявили другой тип (например, модель Pydantic).

В таком случае можно использовать параметр `response_model` внутри *декоратора операции пути* вместо аннотации возвращаемого значения функции.

Параметр `response_model` может быть указан для любой *операции пути*:

* `@app.get()`
* `@app.post()`
* `@app.put()`
* `@app.delete()`
* и др.

//// tab | Python 3.10+

```Python hl_lines="17  22  24-27"
{!> ../../docs_src/response_model/tutorial001_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="17  22  24-27"
{!> ../../docs_src/response_model/tutorial001_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="17  22  24-27"
{!> ../../docs_src/response_model/tutorial001.py!}
```

////

/// note | "Технические детали"

Помните, что параметр `response_model` является параметром именно декоратора http-методов (`get`, `post`, и т.п.). Не следует его указывать для *функций операций пути*, как вы бы поступили с другими параметрами или с телом запроса.

///

`response_model` принимает те же типы, которые можно указать для какого-либо поля в модели Pydantic. Таким образом, это может быть как одиночная модель Pydantic, так и `список (list)` моделей Pydantic. Например, `List[Item]`.

FastAPI будет использовать значение `response_model` для того, чтобы автоматически генерировать документацию, производить валидацию и т.п. А также для **конвертации и фильтрации выходных данных** в объявленный тип.

/// tip | "Подсказка"

Если вы используете анализаторы типов со строгой проверкой (например, mypy), можно указать `Any` в качестве типа возвращаемого значения функции.

Таким образом вы информируете ваш редактор кода, что намеренно возвращаете данные неопределенного типа. Но возможности FastAPI, такие как автоматическая генерация документации, валидация, фильтрация и т.д. все так же будут работать, просто используя параметр `response_model`.

///

### Приоритет `response_model`

Если одновременно указать аннотацию типа для ответа функции и параметр `response_model` - последний будет иметь больший приоритет и FastAPI будет использовать именно его.

Таким образом вы можете объявить корректные аннотации типов к вашим функциям, даже если они возвращают тип, отличающийся от указанного в `response_model`. Они будут считаны во время статической проверки типов вашими помощниками, например, mypy. При этом вы все так же используете возможности FastAPI для автоматической документации, валидации и т.д. благодаря `response_model`.

Вы можете указать значение `response_model=None`, чтобы отключить создание модели ответа для данной *операции пути*. Это может понадобиться, если вы добавляете аннотации типов для данных, не являющихся валидными полями Pydantic. Мы увидим пример кода для такого случая в одном из разделов ниже.

## Получить и вернуть один и тот же тип данных

Здесь мы объявили модель `UserIn`, которая хранит пользовательский пароль в открытом виде:

//// tab | Python 3.10+

```Python hl_lines="7  9"
{!> ../../docs_src/response_model/tutorial002_py310.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="9  11"
{!> ../../docs_src/response_model/tutorial002.py!}
```

////

/// info | "Информация"

Чтобы использовать `EmailStr`, прежде необходимо установить <a href="https://github.com/JoshData/python-email-validator" class="external-link" target="_blank">`email-validator`</a>.
Используйте `pip install email-validator`
или `pip install pydantic[email]`.

///

Далее мы используем нашу модель в аннотациях типа как для аргумента функции, так и для выходного значения:

//// tab | Python 3.10+

```Python hl_lines="16"
{!> ../../docs_src/response_model/tutorial002_py310.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="18"
{!> ../../docs_src/response_model/tutorial002.py!}
```

////

Теперь всякий раз, когда клиент создает пользователя с паролем, API будет возвращать его пароль в ответе.

В данном случае это не такая уж большая проблема, поскольку ответ получит тот же самый пользователь, который и создал пароль.

Но что если мы захотим использовать эту модель для какой-либо другой *операции пути*? Мы можем, сами того не желая, отправить пароль любому другому пользователю.

/// danger | "Осторожно"

Никогда не храните пароли пользователей в открытом виде, а также никогда не возвращайте их в ответе, как в примере выше. В противном случае - убедитесь, что вы хорошо продумали и учли все возможные риски такого подхода и вам известно, что вы делаете.

///

## Создание модели для ответа

Вместо этого мы можем создать входную модель, хранящую пароль в открытом виде и выходную модель без пароля:

//// tab | Python 3.10+

```Python hl_lines="9  11  16"
{!> ../../docs_src/response_model/tutorial003_py310.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="9  11  16"
{!> ../../docs_src/response_model/tutorial003.py!}
```

////

В таком случае, даже несмотря на то, что наша *функция операции пути* возвращает тот же самый объект пользователя с паролем, полученным на вход:

//// tab | Python 3.10+

```Python hl_lines="24"
{!> ../../docs_src/response_model/tutorial003_py310.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="24"
{!> ../../docs_src/response_model/tutorial003.py!}
```

////

...мы указали в `response_model` модель `UserOut`, в которой отсутствует поле, содержащее пароль - и он будет исключен из ответа:

//// tab | Python 3.10+

```Python hl_lines="22"
{!> ../../docs_src/response_model/tutorial003_py310.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="22"
{!> ../../docs_src/response_model/tutorial003.py!}
```

////

Таким образом **FastAPI** позаботится о фильтрации ответа и исключит из него всё, что не указано в выходной модели (при помощи Pydantic).

### `response_model` или возвращаемый тип данных

В нашем примере модели входных данных и выходных данных различаются. И если мы укажем аннотацию типа выходного значения функции как `UserOut` - проверка типов выдаст ошибку из-за того, что мы возвращаем некорректный тип. Поскольку это 2 разных класса.

Поэтому в нашем примере мы можем объявить тип ответа только в параметре `response_model`.

...но продолжайте читать дальше, чтобы узнать как можно это обойти.

## Возвращаемый тип и Фильтрация данных

Продолжим рассматривать предыдущий пример. Мы хотели **аннотировать входные данные одним типом**, а выходное значение - **другим типом**.

Мы хотим, чтобы FastAPI продолжал **фильтровать** данные, используя `response_model`.

В прошлом примере, т.к. входной и выходной типы являлись разными классами, мы были вынуждены использовать параметр `response_model`. И как следствие, мы лишались помощи статических анализаторов для проверки ответа функции.

Но в подавляющем большинстве случаев мы будем хотеть, чтобы модель ответа лишь **фильтровала/удаляла** некоторые данные из ответа, как в нашем примере.

И в таких случаях мы можем использовать классы и наследование, чтобы пользоваться преимуществами **аннотаций типов** и получать более полную статическую проверку типов. Но при этом все так же получать **фильтрацию ответа** от FastAPI.

//// tab | Python 3.10+

```Python hl_lines="7-10  13-14  18"
{!> ../../docs_src/response_model/tutorial003_01_py310.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="9-13  15-16  20"
{!> ../../docs_src/response_model/tutorial003_01.py!}
```

////

Таким образом, мы получаем поддержку редактора кода и mypy в части типов, сохраняя при этом фильтрацию данных от FastAPI.

Как это возможно? Давайте разберемся. 🤓

### Аннотации типов и инструменты для их проверки

Для начала давайте рассмотрим как наш редактор кода, mypy и другие помощники разработчика видят аннотации типов.

У модели `BaseUser` есть некоторые поля. Затем `UserIn` наследуется от `BaseUser` и добавляет новое поле `password`. Таким образом модель будет включать в себя все поля из первой модели (родителя), а также свои собственные.

Мы аннотируем возвращаемый тип функции как `BaseUser`, но фактически мы будем возвращать объект типа `UserIn`.

Редакторы, mypy и другие инструменты не будут иметь возражений против такого подхода, поскольку `UserIn` является подклассом `BaseUser`. Это означает, что такой тип будет *корректным*, т.к. ответ может быть чем угодно, если это будет `BaseUser`.

### Фильтрация Данных FastAPI

FastAPI знает тип ответа функции, так что вы можете быть уверены, что на выходе будут **только** те поля, которые вы указали.

FastAPI совместно с Pydantic выполнит некоторую магию "под капотом", чтобы убедиться, что те же самые правила наследования классов не используются для фильтрации возвращаемых данных, в противном случае вы могли бы в конечном итоге вернуть гораздо больше данных, чем ожидали.

Таким образом, вы можете получить все самое лучшее из обоих миров: аннотации типов с **поддержкой инструментов для разработки** и **фильтрацию данных**.

## Автоматическая документация

Если посмотреть на сгенерированную документацию, вы можете убедиться, что в ней присутствуют обе JSON схемы - как для входной модели, так и для выходной:

<img src="/img/tutorial/response-model/image01.png">

И также обе модели будут использованы в интерактивной документации API:

<img src="/img/tutorial/response-model/image02.png">

## Другие аннотации типов

Бывают случаи, когда вы возвращаете что-то, что не является валидным типом для Pydantic и вы указываете аннотацию ответа функции только для того, чтобы работала поддержка различных инструментов (редактор кода, mypy и др.).

### Возвращаем Response

Самый частый сценарий использования - это [возвращать Response напрямую, как описано в расширенной документации](../advanced/response-directly.md){.internal-link target=_blank}.

```Python hl_lines="8  10-11"
{!> ../../docs_src/response_model/tutorial003_02.py!}
```

Это поддерживается FastAPI по-умолчанию, т.к. аннотация проставлена в классе (или подклассе) `Response`.

И ваши помощники разработки также будут счастливы, т.к. оба класса `RedirectResponse` и `JSONResponse` являются подклассами `Response`. Таким образом мы получаем корректную аннотацию типа.

### Подкласс Response в аннотации типа

Вы также можете указать подкласс `Response` в аннотации типа:

```Python hl_lines="8-9"
{!> ../../docs_src/response_model/tutorial003_03.py!}
```

Это сработает, потому что `RedirectResponse` является подклассом `Response` и FastAPI автоматически обработает этот простейший случай.

### Некорректные аннотации типов

Но когда вы возвращаете какой-либо другой произвольный объект, который не является допустимым типом Pydantic (например, объект из базы данных), и вы аннотируете его подобным образом для функции, FastAPI попытается создать из этого типа модель Pydantic и потерпит неудачу.

То же самое произошло бы, если бы у вас было что-то вроде <abbr title='Union разных типов буквально означает "любой из перечисленных типов".'>Union</abbr> различных типов и один или несколько из них не являлись бы допустимыми типами для Pydantic. Например, такой вариант приведет к ошибке 💥:

//// tab | Python 3.10+

```Python hl_lines="8"
{!> ../../docs_src/response_model/tutorial003_04_py310.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="10"
{!> ../../docs_src/response_model/tutorial003_04.py!}
```

////

...такой код вызовет ошибку, потому что в аннотации указан неподдерживаемый Pydantic тип. А также этот тип не является классом или подклассом `Response`.

### Возможно ли отключить генерацию модели ответа?

Продолжим рассматривать предыдущий пример. Допустим, что вы хотите отказаться от автоматической валидации ответа, документации, фильтрации и т.д.

Но в то же время, хотите сохранить аннотацию возвращаемого типа для функции, чтобы обеспечить работу помощников и анализаторов типов (например, mypy).

В таком случае, вы можете отключить генерацию модели ответа, указав `response_model=None`:

//// tab | Python 3.10+

```Python hl_lines="7"
{!> ../../docs_src/response_model/tutorial003_05_py310.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="9"
{!> ../../docs_src/response_model/tutorial003_05.py!}
```

////

Тогда FastAPI не станет генерировать модель ответа и вы сможете сохранить такую аннотацию типа, которая вам требуется, никак не влияя на работу FastAPI. 🤓

## Параметры модели ответа

Модель ответа может иметь значения по умолчанию, например:

//// tab | Python 3.10+

```Python hl_lines="9  11-12"
{!> ../../docs_src/response_model/tutorial004_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="11  13-14"
{!> ../../docs_src/response_model/tutorial004_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="11  13-14"
{!> ../../docs_src/response_model/tutorial004.py!}
```

////

* `description: Union[str, None] = None` (или `str | None = None` в Python 3.10), где `None` является значением по умолчанию.
* `tax: float = 10.5`, где `10.5` является значением по умолчанию.
* `tags: List[str] = []`, где пустой список `[]` является значением по умолчанию.

но вы, возможно, хотели бы исключить их из ответа, если данные поля не были заданы явно.

Например, у вас есть модель с множеством необязательных полей в NoSQL базе данных, но вы не хотите отправлять в качестве ответа очень длинный JSON с множеством значений по умолчанию.

### Используйте параметр `response_model_exclude_unset`

Установите для *декоратора операции пути* параметр `response_model_exclude_unset=True`:

//// tab | Python 3.10+

```Python hl_lines="22"
{!> ../../docs_src/response_model/tutorial004_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="24"
{!> ../../docs_src/response_model/tutorial004_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="24"
{!> ../../docs_src/response_model/tutorial004.py!}
```

////

и тогда значения по умолчанию не будут включены в ответ. В нем будут только те поля, значения которых фактически были установлены.

Итак, если вы отправите запрос на данную *операцию пути* для элемента, с ID = `Foo` - ответ (с исключенными значениями по-умолчанию) будет таким:

```JSON
{
    "name": "Foo",
    "price": 50.2
}
```

/// info | "Информация"

"Под капотом" FastAPI использует метод `.dict()` у объектов моделей Pydantic <a href="https://docs.pydantic.dev/latest/concepts/serialization/#modeldict" class="external-link" target="_blank">с параметром `exclude_unset`</a>, чтобы достичь такого эффекта.

///

/// info | "Информация"

Вы также можете использовать:

* `response_model_exclude_defaults=True`
* `response_model_exclude_none=True`

как описано в <a href="https://docs.pydantic.dev/latest/concepts/serialization/#modeldict" class="external-link" target="_blank">документации Pydantic</a> для параметров `exclude_defaults` и `exclude_none`.

///

#### Если значение поля отличается от значения по-умолчанию

Если для некоторых полей модели, имеющих значения по-умолчанию, значения были явно установлены - как для элемента с ID = `Bar`, ответ будет таким:

```Python hl_lines="3  5"
{
    "name": "Bar",
    "description": "The bartenders",
    "price": 62,
    "tax": 20.2
}
```

они не будут исключены из ответа.

#### Если значение поля совпадает с его значением по умолчанию

Если данные содержат те же значения, которые являются для этих полей по умолчанию, но были установлены явно - как для элемента с ID = `baz`, ответ будет таким:

```Python hl_lines="3  5-6"
{
    "name": "Baz",
    "description": None,
    "price": 50.2,
    "tax": 10.5,
    "tags": []
}
```

FastAPI достаточно умен (на самом деле, это заслуга Pydantic), чтобы понять, что, хотя `description`, `tax` и `tags` хранят такие же данные, какие должны быть по умолчанию - для них эти значения были установлены явно (а не получены из значений по умолчанию).

И поэтому, они также будут включены в JSON ответа.

/// tip | "Подсказка"

Значением по умолчанию может быть что угодно, не только `None`.

Им может быть и список (`[]`), значение 10.5 типа `float`, и т.п.

///

### `response_model_include` и `response_model_exclude`

Вы также можете использовать параметры *декоратора операции пути*, такие, как `response_model_include` и `response_model_exclude`.

Они принимают аргументы типа `set`, состоящий из строк (`str`) с названиями атрибутов, которые либо требуется включить в ответ (при этом исключив все остальные), либо  наоборот исключить (оставив в ответе все остальные поля).

Это можно использовать как быстрый способ исключить данные из ответа, не создавая отдельную модель Pydantic.

/// tip | "Подсказка"

Но по-прежнему рекомендуется следовать изложенным выше советам и использовать несколько моделей вместо данных параметров.

Потому как JSON схема OpenAPI, генерируемая вашим приложением (а также документация) все еще будет содержать все поля, даже если вы использовали `response_model_include` или `response_model_exclude` и исключили некоторые атрибуты.

То же самое применимо к параметру `response_model_by_alias`.

///

//// tab | Python 3.10+

```Python hl_lines="29  35"
{!> ../../docs_src/response_model/tutorial005_py310.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="31  37"
{!> ../../docs_src/response_model/tutorial005.py!}
```

////

/// tip | "Подсказка"

При помощи кода `{"name","description"}` создается объект множества (`set`) с двумя строковыми значениями.

Того же самого можно достичь используя `set(["name", "description"])`.

///

#### Что если использовать `list` вместо `set`?

Если вы забыли про `set` и использовали структуру `list` или `tuple`, FastAPI автоматически преобразует этот объект в `set`, чтобы обеспечить корректную работу:

//// tab | Python 3.10+

```Python hl_lines="29  35"
{!> ../../docs_src/response_model/tutorial006_py310.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="31  37"
{!> ../../docs_src/response_model/tutorial006.py!}
```

////

## Резюме

Используйте параметр `response_model` у *декоратора операции пути* для того, чтобы задать модель ответа и в большей степени для того, чтобы быть уверенным, что приватная информация будет отфильтрована.

А также используйте `response_model_exclude_unset`, чтобы возвращать только те значения, которые были заданы явно.