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
import type { LoginRequest } from '@/api/types/types'
import { useRouter } from 'vue-router'
import Spinner from '@/components/ui/spinner/Spinner.vue'

const props = defineProps<{
  class?: HTMLAttributes['class']
}>()

const schema = toTypedSchema(
  zod.object({
    nombre: zod
      .string()
      .min(1, 'Este campo es obligatorio')
      .min(4, 'Mínimo 4 caracteres')
      .max(20, 'Máximo 20 caracteres'),
    contraseña: zod.string().min(1, 'Este campo es obligatorio').min(6, 'Mínimo 6 caracteres'),
  }),
)

const { handleSubmit, errors } = useForm({ validationSchema: schema })

const { value: nombre } = useField('nombre', undefined, { initialValue: '' })
const { value: contraseña } = useField('contraseña', undefined, { initialValue: '' })

const authStore = useAuthStore()
const router = useRouter()

const onSubmit = handleSubmit(async (data: LoginRequest) => {
  const success = await authStore.iniciarSesion(data)

  if (success) {
    router.push({ name: 'archivos' })
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

          <h1 class="text-xl font-bold">Bienvenido de nuevo</h1>

          <FieldDescription>
            ¿No tienes una cuenta? <RouterLink :to="{ name: 'register' }">Crear Cuenta</RouterLink>
          </FieldDescription>
        </div>

        <Field>
          <FieldLabel for="nombre"> Nombre* </FieldLabel>
          <Input id="nombre" type="text" placeholder="usuario" v-model="nombre" />
          <FieldError v-if="errors.nombre">{{ errors.nombre }}</FieldError>
        </Field>

        <Field>
          <FieldLabel for="contraseña"> Contraseña* </FieldLabel>
          <Input id="contraseña" type="password" placeholder="***********" v-model="contraseña" />
          <FieldError v-if="errors.contraseña">{{ errors.contraseña }}</FieldError>
        </Field>

        <Field>
          <Button type="submit" class="hover:cursor-pointer" :disabled="authStore.cargando">
            <Spinner v-if="authStore.cargando" />
            {{ !authStore.cargando ? 'Iniciar Sesión' : 'Cargando...' }}
          </Button>
        </Field>
      </FieldGroup>
    </form>

    <FieldDescription class="px-6 text-center">
      Al hacer click en continuar, aceptas nuestros <a href="#">Términos de Servicio</a> y
      <a href="#">Política de Privacidad</a>.
    </FieldDescription>
  </div>
</template>
