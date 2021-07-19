  const inputs = document.querySelectorAll(".input");


  function addcl() {
      let parent = this.parentNode.parentNode;
      parent.classList.add("focus");
  }

  function remcl() {
      let parent = this.parentNode.parentNode;
      if (this.value == "") {
          parent.classList.remove("focus");
      }
  }


  inputs.forEach(input => {
      input.addEventListener("focus", addcl);
      input.addEventListener("blur", remcl);
  });


  //  ========================
  //   INICIO GR[AFICA
  //  ========================
  let a = 0;
  let paises = ['Guatemala', 'Costa Rica', 'Panamá', 'Nicaragua', 'El Salvador'];
  let countpaises = [];

  console.log("PRUEBA");
  console.log("{{editar}}");



  var ctx = document.getElementById('myChart');
  var myChart = new Chart(ctx, {
      type: 'pie',
      data: {
          labels: ['Guatemala', 'Costa Rica', 'Panamá', 'Nicaragua', 'El Salvador'],
          datasets: [{
              label: '# of Votes',
              data: [12, 19, 3, 5, 2],
              backgroundColor: [
                  'rgba(255, 99, 132, 0.5)',
                  'rgba(54, 162, 235, 0.5)',
                  'rgba(255, 206, 86, 0.5)',
                  'rgba(75, 192, 192, 0.5)',
                  'rgba(153, 102, 255, 0.5)',
              ],
              borderColor: [
                  'rgba(255, 99, 132, 1)',
                  'rgba(54, 162, 235, 1)',
                  'rgba(255, 206, 86, 1)',
                  'rgba(75, 192, 192, 1)',
                  'rgba(153, 102, 255, 1)',
              ],
              borderWidth: 1
          }]
      },
      options: {
          scales: {
              y: {
                  beginAtZero: true
              }
          }
      }
  });
  //  ========================
  //   FIN GR[AFICA
  //  ========================