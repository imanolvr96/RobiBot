import { Component, OnInit } from '@angular/core';

import { Cita } from 'src/app/cita';
import { CitaService } from 'src/app/cita.service';


@Component({
  selector: 'app-vista-citas',
  templateUrl: './vista-citas.component.html',
  styleUrls: ['./vista-citas.component.css']
})
export class VistaCitasComponent implements OnInit {

  citas: Cita[] = [];

  constructor(private citaService: CitaService) { }

  ngOnInit() {

    this.getCitas();
  }

  getCitas(): void {

    this.citaService.getCitas().subscribe(citas => this.citas = citas);
  }

  delete(cita: Cita): void {
    this.citaService.deleteReserv(cita).subscribe(success => {this.getCitas(); });
  }
}
