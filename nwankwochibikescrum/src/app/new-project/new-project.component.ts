import { Component, OnInit } from '@angular/core';
import {DataService} from "../data.service";

@Component({
  selector: 'app-new-project',
  templateUrl: './new-project.component.html',
  styleUrls: ['./new-project.component.css']
})
export class NewProjectComponent implements OnInit {
  public dataService: DataService

  constructor(private _dataService: DataService) { this.dataService = this._dataService }

  ngOnInit() {
  }

}
