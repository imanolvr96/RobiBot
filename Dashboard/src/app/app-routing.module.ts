import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { InicioComponent } from './componentes/inicio/inicio.component';
import { CitasComponent } from './componentes/citas/citas.component';
import { HorarioComponent } from './componentes/horario/horario.component';


const routes: Routes = [
    {
        path: 'inicio',
        component: InicioComponent
    },
    {
        path: 'citas',
        component: CitasComponent
    },
    {
        path: 'horario',
        component: HorarioComponent
    },
    {
        path: '',
        redirectTo: '/inicio', pathMatch: 'full'

    }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
