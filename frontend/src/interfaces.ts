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

export interface ComponentUpdateItf {
  type: string;
}

export interface ChatUpdateItf extends ComponentUpdateItf {}

export interface ChatNewLineItf extends ChatUpdateItf {
  line: string;
}

export interface ChatSubmitLineItf extends ChatUpdateItf {
  line: string;
}

export interface ComponentUpdateDetailsItf {
  componentId: string;
  componentUpdate: ComponentUpdateItf;
}

export interface UpdateComponentUpdateItf extends UpdateItf {
  details: ComponentUpdateDetailsItf;
}

export interface SceneUpdateDetailsItf {
  components: ComponentItf[];
}

export interface SetSceneUpdateItf extends UpdateItf {
  details: SceneUpdateDetailsItf;
}
