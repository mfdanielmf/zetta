import {
  File,
  FileText,
  FileImage,
  FileVideo,
  FileAudio,
  FileArchive,
  FileSpreadsheet,
  FileCode,
  type LucideIcon,
} from 'lucide-vue-next'

const map: Record<string, LucideIcon> = {
  pdf: FileText,
  doc: FileText,
  docx: FileText,
  txt: FileText,

  png: FileImage,
  jpg: FileImage,
  jpeg: FileImage,
  gif: FileImage,
  webp: FileImage,

  mp4: FileVideo,
  mov: FileVideo,
  avi: FileVideo,

  mp3: FileAudio,
  wav: FileAudio,

  zip: FileArchive,
  rar: FileArchive,
  tar: FileArchive,

  xls: FileSpreadsheet,
  xlsx: FileSpreadsheet,
  csv: FileSpreadsheet,

  js: FileCode,
  ts: FileCode,
  json: FileCode,
  html: FileCode,
  css: FileCode,
}

export default function getIconExtension(nombre: string): LucideIcon {
  const extension = nombre.split('.').pop()?.toLowerCase() ?? ''

  return map[extension] ?? File
}
