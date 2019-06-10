import { Component, OnInit } from '@angular/core';

import { Horario } from 'src/app/horario';
import { HorarioService } from 'src/app/horaio.service';


@Component({
  selector: 'app-vista-horario',
  templateUrl: './vista-horario.component.html',
  styleUrls: ['./vista-horario.component.css']
})

export class VistaHorarioComponent implements OnInit {

  horarios: Horario[] = [];

  constructor(private horarioService: HorarioService) { }

  ngOnInit() {
    this.getHorarios();
  }

  getHorarios(): void {

    this.horarioService.getHorarios().subscribe(horarios => this.horarios = horarios);
  }

  delete(horaio: Horario): void {
    this.horarioService.deleteHour(horaio).subscribe(success => {this.getHorarios(); });
  }
}