import type { LucideIcon } from 'lucide-react'
import { FileText, Inbox, Shield, Cpu, UsersRound, Quote, Users } from 'lucide-react'

export type FieldType = 'text' | 'textarea' | 'richtext' | 'number' | 'boolean' | 'select' | 'image' | 'tags' | 'password'

export interface FieldOption {
  label: string
  value: string
}

export interface FieldConfig {
  name: string
  label: string
  type: FieldType
  options?: FieldOption[]
  required?: boolean
  hideInTable?: boolean
}

export interface ModuleConfig {
  key: string
  label: string
  icon: LucideIcon
  apiPath: string
  fields: FieldConfig[]
  canCreate?: boolean
  canDelete?: boolean
  roles?: string[]
  emptyLabel?: string
}

/**
 * ============================================================================
 *  PONTO ÚNICO DE CONFIGURAÇÃO DO BACK OFFICE
 * ============================================================================
 *
 * Esta lista é a única coisa que a interface do Back Office lê para saber
 * que módulos existem, que campos cada um tem, e como desenhar a tabela e o
 * formulário. Não há nenhum ecrã "codificado à mão" por módulo.
 *
 * Para acrescentar uma NOVA funcionalidade/opção ao Back Office:
 *
 *   1. Criar o módulo correspondente no backend
 *      (modelo + schema + router — ver backend/app/core/module_registry.py,
 *      ou correr `python scripts/new_module.py --name X --label Y --fields ...`)
 *
 *   2. Acrescentar aqui, no array MODULES, um novo objeto ModuleConfig.
 *
 * Isso é tudo. A tabela, o formulário, o menu lateral e o painel de
 * contagens no Dashboard atualizam-se sozinhos a partir desta configuração.
 * ============================================================================
 */
export const MODULES: ModuleConfig[] = [
  {
    key: 'blog',
    label: 'Blog',
    icon: FileText,
    apiPath: '/blog',
    fields: [
      { name: 'titulo', label: 'Título', type: 'text', required: true },
      { name: 'slug', label: 'Slug (URL)', type: 'text', required: true },
      { name: 'resumo', label: 'Resumo', type: 'textarea' },
      { name: 'conteudo', label: 'Conteúdo', type: 'richtext', required: true, hideInTable: true },
      { name: 'imagem_capa', label: 'Imagem de capa (URL)', type: 'image', hideInTable: true },
      { name: 'categoria', label: 'Categoria', type: 'text' },
      { name: 'autor', label: 'Autor', type: 'text' },
      {
        name: 'estado', label: 'Estado', type: 'select',
        options: [
          { label: 'Rascunho', value: 'rascunho' },
          { label: 'Publicado', value: 'publicado' },
        ],
      },
    ],
  },
  {
    key: 'leads',
    label: 'Contactos / Leads',
    icon: Inbox,
    apiPath: '/leads',
    canCreate: false,
    emptyLabel: 'Ainda não há submissões do formulário de contacto do site.',
    fields: [
      { name: 'nome', label: 'Nome', type: 'text', required: true },
      { name: 'email', label: 'Email', type: 'text', required: true },
      { name: 'empresa', label: 'Empresa', type: 'text' },
      { name: 'telefone', label: 'Telefone', type: 'text' },
      { name: 'tipo_pedido', label: 'Tipo de pedido', type: 'text' },
      { name: 'mensagem', label: 'Mensagem', type: 'textarea', hideInTable: true },
      {
        name: 'estado', label: 'Estado', type: 'select',
        options: [
          { label: 'Novo', value: 'novo' },
          { label: 'Em contacto', value: 'em_contacto' },
          { label: 'Convertido', value: 'convertido' },
          { label: 'Arquivado', value: 'arquivado' },
        ],
      },
      { name: 'notas_internas', label: 'Notas internas', type: 'textarea', hideInTable: true },
    ],
  },
  {
    key: 'services',
    label: 'Serviços',
    icon: Shield,
    apiPath: '/services',
    fields: [
      { name: 'titulo', label: 'Título', type: 'text', required: true },
      { name: 'descricao', label: 'Descrição', type: 'textarea' },
      { name: 'icone', label: 'Ícone', type: 'text' },
      { name: 'ordem', label: 'Ordem', type: 'number' },
      { name: 'ativo', label: 'Ativo no site', type: 'boolean' },
    ],
  },
  {
    key: 'products',
    label: 'Produtos',
    icon: Cpu,
    apiPath: '/products',
    fields: [
      { name: 'nome', label: 'Nome', type: 'text', required: true },
      { name: 'tagline', label: 'Tagline', type: 'text' },
      { name: 'descricao', label: 'Descrição', type: 'textarea' },
      { name: 'features', label: 'Funcionalidades (separadas por vírgula)', type: 'tags' },
      { name: 'link_externo', label: 'Link externo', type: 'text' },
      { name: 'icone', label: 'Ícone', type: 'text' },
      { name: 'ordem', label: 'Ordem', type: 'number' },
      { name: 'ativo', label: 'Ativo no site', type: 'boolean' },
    ],
  },
  {
    key: 'team',
    label: 'Equipa',
    icon: UsersRound,
    apiPath: '/team',
    fields: [
      { name: 'nome', label: 'Nome', type: 'text', required: true },
      { name: 'cargo', label: 'Cargo', type: 'text' },
      { name: 'foto', label: 'Foto (URL)', type: 'image' },
      { name: 'bio', label: 'Bio', type: 'textarea', hideInTable: true },
      { name: 'linkedin', label: 'LinkedIn', type: 'text' },
      { name: 'ordem', label: 'Ordem', type: 'number' },
      { name: 'ativo', label: 'Ativo no site', type: 'boolean' },
    ],
  },
  {
    key: 'testimonials',
    label: 'Testemunhos',
    icon: Quote,
    apiPath: '/testimonials',
    fields: [
      { name: 'nome', label: 'Nome', type: 'text', required: true },
      { name: 'empresa', label: 'Empresa', type: 'text' },
      { name: 'cargo', label: 'Cargo', type: 'text' },
      { name: 'texto', label: 'Texto', type: 'textarea', required: true, hideInTable: true },
      { name: 'foto', label: 'Foto (URL)', type: 'image' },
      { name: 'ordem', label: 'Ordem', type: 'number' },
      { name: 'ativo', label: 'Ativo no site', type: 'boolean' },
    ],
  },
  {
    key: 'users',
    label: 'Utilizadores',
    icon: Users,
    apiPath: '/users',
    roles: ['admin'],
    fields: [
      { name: 'nome', label: 'Nome', type: 'text', required: true },
      { name: 'email', label: 'Email', type: 'text', required: true },
      {
        name: 'role', label: 'Função', type: 'select',
        options: [
          { label: 'Administrador', value: 'admin' },
          { label: 'Editor', value: 'editor' },
          { label: 'Leitor', value: 'viewer' },
        ],
      },
      { name: 'password', label: 'Password', type: 'password', hideInTable: true },
      { name: 'ativo', label: 'Ativo', type: 'boolean' },
    ],
  },
]
