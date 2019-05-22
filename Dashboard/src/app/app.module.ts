import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { CabeceraComponent } from './componentes/cabecera/cabecera.component';
import { MenuComponent } from './componentes/menu/menu.component';
import { InicioComponent } from './componentes/inicio/inicio.component';
import { CitasComponent } from './componentes/citas/citas.component';
import { HorarioComponent } from './componentes/horario/horario.component';
import { VistaHorarioComponent } from './componentes/vista-horario/vista-horario.component';


@NgModule({
  declarations: [
    AppComponent,
    CabeceraComponent,
    MenuComponent,
    InicioComponent,
    CitasComponent,
    HorarioComponent,
    VistaHorarioComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
