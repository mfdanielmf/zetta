<script setup lang="ts">
import { Button } from '@/components/ui/button'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'
import { Field, FieldLabel, FieldError } from '@/components/ui/field'
import Input from '../ui/input/Input.vue'

import * as zod from 'zod'
import { toTypedSchema } from '@vee-validate/zod'
import { useField, useForm } from 'vee-validate'

const schema = toTypedSchema(
  zod.object({
    nombre: zod.string().min(1, 'Este campo es obligatorio').max(100, 'Máximo 100 caracteres'),
  }),
)

const { handleSubmit, errors } = useForm({ validationSchema: schema })

const { value: nombre } = useField('nombre', undefined, { initialValue: '' })

const onSubmit = handleSubmit((data) => {
  console.log(data.nombre)
})
</script>

<template>
  <Dialog>
    <DialogContent class="sm:max-w-106.25">
      <DialogHeader>
        <DialogTitle>Crear carpeta</DialogTitle>
        <DialogDescription>Introduce el nombre de la nueva carpeta</DialogDescription>
      </DialogHeader>

      <form @submit="onSubmit">
        <Field>
          <FieldLabel for="nombre"> Nombre* </FieldLabel>
          <Input id="nombre" type="text" placeholder="usuario" v-model="nombre" />
          <FieldError v-if="errors.nombre">{{ errors.nombre }}</FieldError>
        </Field>
      </form>

      <DialogFooter>
        <Button class="hover:cursor-pointer" @click="onSubmit">Crear Carpeta</Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>
