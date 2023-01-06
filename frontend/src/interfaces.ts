import { ComponentType, UpdateDestination, UpdateType } from "./constants";

export interface GameItf {
  id: string;
  name: string;
}

export interface ComponentItf {
  id: string;
  type: ComponentType;
}

export interface ChatComponentItf extends ComponentItf {
  lines: string[];
}

export interface UpdateItf {
  destination: UpdateDestination;
  type: UpdateType;
}

export interface UpdateComponentUpdateItf extends UpdateItf {
  componentId: string;
  data: any;
}

export interface SetComponentsUpdateItf extends UpdateItf {
  components: ComponentItf[];
}
