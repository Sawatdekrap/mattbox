import { ComponentType } from "./constants";

export interface GameItf {
  id: string;
  name: string;
}

export interface ComponentItf {
  id: string;
  type: ComponentType;
}

export interface LayoutItf {
  components: ComponentItf[];
}
