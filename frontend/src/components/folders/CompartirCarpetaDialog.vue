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
import Spinner from '../ui/spinner/Spinner.vue'
import { watch } from 'vue'
import { Share2 } from 'lucide-vue-next'

const props = defineProps<{
  pending: boolean
  reset: boolean
}>()

const emit = defineEmits(['compartirCarpeta'])

watch(
  () => props.reset,
  (nuevoValor) => {
    if (nuevoValor === false) {
      resetForm()
    }
  },
)

const schema = toTypedSchema(
  zod.object({
    correo: zod.string().min(1, 'Este campo es obligatorio').email('Correo incorrecto'),
  }),
)

const { handleSubmit, errors, resetForm } = useForm({ validationSchema: schema })

const { value: correo } = useField('correo', undefined, { initialValue: '' })

const onSubmit = handleSubmit((data) => {
  emit('compartirCarpeta', data.correo)
})
</script>

<template>
  <Dialog>
    <DialogContent class="sm:max-w-106.25">
      <DialogHeader>
        <DialogTitle>Compartir carpeta</DialogTitle>
        <DialogDescription>Comparte una carpeta con cualquier usuario</DialogDescription>
      </DialogHeader>

      <form @submit="onSubmit">
        <Field>
          <FieldLabel for="nombre"> Correo* </FieldLabel>
          <Input id="correo" type="text" placeholder="Correo usuario" v-model="correo" />
          <FieldError v-if="errors.correo">{{ errors.correo }}</FieldError>
        </Field>
      </form>

      <DialogFooter>
        <Button class="hover:cursor-pointer" @click="onSubmit" :disabled="props.pending">
          <Spinner v-if="props.pending" />
          <Share2 v-else />
          {{ props.pending ? 'Compartiendo carpeta...' : 'Compartir' }}
        </Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>
