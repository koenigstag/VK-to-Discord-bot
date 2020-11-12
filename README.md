# VK-to-Discord-bot (updated 2020) [![deepcode](https://www.deepcode.ai/api/gh/badge?key=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwbGF0Zm9ybTEiOiJnaCIsIm93bmVyMSI6ImtvZW5pZ3N0YWciLCJyZXBvMSI6IlZLLXRvLURpc2NvcmQtYm90IiwiaW5jbHVkZUxpbnQiOmZhbHNlLCJhdXRob3JJZCI6MjM4MzEsImlhdCI6MTYwNTIwNjg1NX0.qYZyUZlYC8C7I_xMUoXOI-CgTknRpW-zyMUVA6PeoYI)](https://www.deepcode.ai/app/gh/koenigstag/VK-to-Discord-bot/_/dashboard?utm_content=gh%2Fkoenigstag%2FVK-to-Discord-bot)

Due to VK.com api changes there is a need to call [wall.get](https://vk.com/dev.php?method=wall.get) method with 2 new parameters - access_token (how to get - [constant](https://vkhost.github.io/)) and api_version (currently = 5.124, [versions](https://vk.com/dev/versions)).
This [temporary 24h](https://devman.org/qna/63/kak-poluchit-token-polzovatelja-dlja-vkontakte/) token does not work (IDK why).

Description of fork changes: added handling of pinned post/no pinned post case, remade new post search method from 'timestamp' into 'post_id'.

------------------------------------

Из-за изменений VK.com api есть необходимость вызывать [wall.get](https://vk.com/dev.php?method=wall.get) метод с 2 новыми параметрами - access_token (как получить - [постоянный](https://vkhost.github.io/)) и api_version (текущий = 5.124, [версии](https://vk.com/dev/versions)).
Этот [временный 24ч](https://devman.org/qna/63/kak-poluchit-token-polzovatelja-dlja-vkontakte/) токен не работает (не знаю почему).

Описание изменений в форке: добавлена обработка случая с закрепленным постом/без закрепленного поста, переделан метод проверки новых постов с timestamp (время публикации) на id поста.
