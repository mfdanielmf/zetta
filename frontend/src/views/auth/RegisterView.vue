<script setup lang="ts">
import type { HTMLAttributes } from 'vue'

import { GalleryVerticalEnd } from 'lucide-vue-next'
import { cn } from '@/lib/utils'
import { Button } from '@/components/ui/button'
import { Field, FieldDescription, FieldGroup, FieldLabel, FieldError } from '@/components/ui/field'
import { Input } from '@/components/ui/input'

import * as zod from 'zod'
import { toTypedSchema } from '@vee-validate/zod'
import { useField, useForm } from 'vee-validate'
import { useAuthStore } from '@/stores/auth.store'
import type { UserRequest } from '@/api/types/types'

const props = defineProps<{
  class?: HTMLAttributes['class']
}>()

const schema = toTypedSchema(
  zod
    .object({
      nombre: zod
        .string()
        .min(1, 'Este campo es obligatorio')
        .min(4, 'Mínimo 4 caracteres')
        .max(20, 'Máximo 20 caracteres'),
      correo: zod.string().min(1, 'Este campo es obligatorio').email('Correo incorrecto'),
      contraseña: zod.string().min(1, 'Este campo es obligatorio').min(6, 'Mínimo 6 caracteres'),
      contraseña_repetir: zod.string().min(1, 'Este campo es obligatorio'),
    })
    .refine((data) => data.contraseña === data.contraseña_repetir, {
      message: 'Las contraseñas no coinciden',
      path: ['contraseña_repetir'],
    }),
)

const { handleSubmit, errors } = useForm({ validationSchema: schema })

const { value: nombre } = useField('nombre', undefined, { initialValue: '' })
const { value: correo } = useField('correo', undefined, { initialValue: '' })
const { value: contraseña } = useField('contraseña', undefined, { initialValue: '' })
const { value: contraseña_repetir } = useField('contraseña_repetir', undefined, {
  initialValue: '',
})

const authStore = useAuthStore()

const onSubmit = handleSubmit(async (data: UserRequest) => {
  const success = await authStore.registrarUsuario(data)

  if (success) {
    //Hacer push al login
  }
})
</script>

<template>
  <div :class="cn('flex flex-col gap-6', props.class)">
    <form @submit="onSubmit">
      <FieldGroup>
        <div class="flex flex-col items-center gap-2 text-center">
          <a href="#" class="flex flex-col items-center gap-2 font-medium">
            <div class="flex size-8 items-center justify-center rounded-md">
              <GalleryVerticalEnd class="size-6" />
            </div>

            <span class="sr-only">Zetta</span>
          </a>

          <h1 class="text-xl font-bold">Bienvenido a Zetta</h1>

          <FieldDescription>
            ¿Ya tienes una cuenta? <a href="#">Iniciar Sesión</a>
          </FieldDescription>
        </div>

        <Field>
          <FieldLabel for="nombre"> Nombre* </FieldLabel>
          <Input id="nombre" type="text" placeholder="usuario" v-model="nombre" />
          <FieldError v-if="errors.nombre">{{ errors.nombre }}</FieldError>
        </Field>

        <Field>
          <FieldLabel for="email"> Correo* </FieldLabel>
          <Input id="email" type="email" placeholder="correo@ejemplo.com" v-model="correo" />
          <FieldError v-if="errors.correo">{{ errors.correo }}</FieldError>
        </Field>

        <Field>
          <FieldLabel for="contraseña"> Contraseña* </FieldLabel>
          <Input id="contraseña" type="password" placeholder="***********" v-model="contraseña" />
          <FieldError v-if="errors.contraseña">{{ errors.contraseña }}</FieldError>
        </Field>

        <Field>
          <FieldLabel for="contraseña-repetir"> Repetir Contraseña* </FieldLabel>
          <Input
            id="contraseña-repetir"
            type="password"
            placeholder="***********"
            v-model="contraseña_repetir"
          />
          <FieldError v-if="errors.contraseña_repetir">{{ errors.contraseña_repetir }}</FieldError>
        </Field>

        <Field>
          <Button type="submit" class="hover:cursor-pointer"> Crear Cuenta </Button>
        </Field>
      </FieldGroup>
    </form>

    <FieldDescription class="px-6 text-center">
      Al hacer click en continuar, aceptas nuestros <a href="#">Términos de Servicio</a> y
      <a href="#">Política de Privacidad</a>.
    </FieldDescription>
  </div>
</template>
