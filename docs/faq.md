# FAQ

<details>
<summary>What if I don't have <code>make</code> installed on my machine?</summary>
<br>
You can refer to the <a href="https://github.com/ryansurf/cli-surf/blob/main/makefile">Makefile</a>. 
Instead of running a command like <code>make run</code>, you can run the command below it: <code>poetry run python src/server.py</code>
</details>
<br>

<details>
<summary>What do I do if the linter fails?</summary>
<br>
If the linter fails, you can run <code>make format</code>, which may fix the issues for you! If not, it will tell you
what needs to be fixed in the output.
</details>
<br>

<details>
<summary>What do I do if pytest fails?</summary>
<br>
If pytest fails, make sure you haven't broken anything unintentionally. Often, new changes in code will result in the unit tests breaking. Functions may now be returning different values/types which the tests do not expect. Please, try to debug any tests you may have broken!
</details>
<br>

<details>
<summary>The project doesn't work on my machine. What should I do?</summary>
<br>
cli-surf is a new project, and things break. If you come across any bugs, please submit an <a href="https://github.com/ryansurf/cli-surf/issues/new">issue!</a>
</details>
<br>

<details>
<summary>What is the purpose of this project?</summary>
<br>
I had a small spare monitor that could only display a terminal screen, so I used it to display the weather via <a href="https://github.com/chubin/wttr.in">wttr.in</a>. I like to surf,
and figured it would be useful to display surf data along with the weather. That is where I got the idea for cli-surf!
</details>
<br>

<details>
<summary>I have a question about contributing.</summary>
<br>
Please refer to the <a href="https://github.com/ryansurf/cli-surf/blob/main/CONTRIBUTING.md">contributing</a> file, or ask a question on the Discord/Discussions page.
</details>
<br>