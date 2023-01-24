---
title: "Ploeg van Frank Vellinga"
ploegleider: Vel
template: default
---
  <table class="table">
    {% for member in site.data.ploegen | where_exp: "ploegleider == 'Vel'" }}%}
      <tr>
        <td><a href="{{ renner_id }}.html">{{ member.renner }}</td>
        <td>{{ member.team }}</td>
        <td>{{ member.nationality }}</td>
        <td>{{ member.JPP }}</td>
        <td>{{ member.punten }}</td>
      </tr>
    {% endfor %}
  </table>