import { Component, OnInit } from '@angular/core';


@Component({
  selector: 'app-vista-horario',
  templateUrl: './vista-horario.component.html',
  styleUrls: ['./vista-horario.component.css']
})
export class VistaHorarioComponent implements OnInit {

  fruits: Array<string> = ['Apple', 'Orange', 'Banana'];

  constructor() { }

  ngOnInit() {
  }

}
