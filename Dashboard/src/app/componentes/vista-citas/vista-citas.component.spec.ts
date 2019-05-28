import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { VistaCitasComponent } from './vista-citas.component';

describe('VistaCitasComponent', () => {
  let component: VistaCitasComponent;
  let fixture: ComponentFixture<VistaCitasComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ VistaCitasComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(VistaCitasComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
