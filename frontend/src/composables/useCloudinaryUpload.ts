/**
 * composables/useCloudinaryUpload.ts
 */
import { ref } from 'vue'

export interface CloudinaryUploadResult {
  public_id:     string
  secure_url:    string
  width:         number
  height:        number
  format:        string
  bytes:         number
  resource_type: string
}

interface ISignatureResponse {
  signature:  string
  timestamp:  number
  api_key:    string
  cloud_name: string
  folder:     string
}

const API_BASE         = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000/api/v1'
const ACCESS_TOKEN_KEY = 'ringit_access_token'

const ALLOWED_TYPES = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp', 'image/heic', 'application/pdf']
const MAX_BYTES     = 10 * 1024 * 1024

const uploading      = ref(false)
const uploadProgress = ref(0)
const error          = ref<string | null>(null)

async function apiFetch<T>(path: string, options: RequestInit = {}, withAuth = false): Promise<T> {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string> ?? {}),
  }
  if (withAuth) {
    const token = localStorage.getItem(ACCESS_TOKEN_KEY)
    if (token) headers['Authorization'] = `Bearer ${token}`
  }
  const res = await fetch(`${API_BASE}${path}`, { ...options, headers })
  if (!res.ok) {
    const body = await res.json().catch(() => ({}))
    const err  = new Error(body?.detail ?? `Request failed: ${res.status}`) as Error & { status: number }
    err.status = res.status
    throw err
  }
  if (res.status === 204) return undefined as T
  return res.json() as Promise<T>
}

export function useCloudinaryUpload() {
  function clearError(): void {
    error.value          = null
    uploadProgress.value = 0
  }

  function validateFile(file: File): void {
    // Accept image/jpg as well as image/jpeg since browsers report both
    const mime = file.type.toLowerCase()
    const isAllowed = ALLOWED_TYPES.includes(mime) || mime.startsWith('image/')
    if (!isAllowed) {
      throw new Error('Invalid file type. Upload a JPG, PNG, WebP, HEIC, or PDF.')
    }
    if (file.size > MAX_BYTES) {
      throw new Error('File too large. Maximum size is 10 MB.')
    }
  }

  async function uploadFile(file: File): Promise<CloudinaryUploadResult> {
    validateFile(file)
    uploading.value      = true
    uploadProgress.value = 0
    error.value          = null
    try {
      const sig = await apiFetch<ISignatureResponse>('/transactions/cloudinary-signature', {}, true)
      uploadProgress.value = 20
  
      const formData = new FormData()
      formData.append('file', file)
      formData.append('api_key', sig.api_key)
      formData.append('timestamp', String(sig.timestamp))
      formData.append('signature', sig.signature)
      formData.append('folder', sig.folder)
      formData.append('allowed_formats', 'jpg,jpeg,png,webp,heic,pdf')
      formData.append('eager', 'c_limit,w_1200,f_auto,q_auto')
  
      const res = await fetch(
        `https://api.cloudinary.com/v1_1/${sig.cloud_name}/image/upload`,
        { method: 'POST', body: formData },
      )
      uploadProgress.value = 90
  
      if (!res.ok) {
        const body = await res.json().catch(() => ({}))
        throw new Error(body?.error?.message ?? 'Cloudinary upload failed.')
      }
  
      const result: CloudinaryUploadResult = await res.json()
      uploadProgress.value = 100
      return result
    } catch (e: unknown) {
      error.value = e instanceof Error ? e.message : 'Upload failed. Please try again.'
      throw e
    } finally {
      uploading.value = false
    }
  }
  
  async function uploadReceipt(file: File): Promise<string> {
    const result = await uploadFile(file)
    return result.secure_url
  }
  
  async function uploadAvatar(file: File): Promise<string> {
    const result = await uploadFile(file)
    return result.secure_url
  }

  return {
    uploading,
    uploadProgress,
    error,
    uploadFile,
    uploadReceipt,
    uploadAvatar,
    clearError,
  }
}