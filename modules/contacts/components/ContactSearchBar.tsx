// Contact search bar component

interface ContactSearchBarProps {
  value: string
  onChange: (value: string) => void
  placeholder?: string
}

export function ContactSearchBar({ value, onChange, placeholder = "Search contacts..." }: ContactSearchBarProps) {
  return (
    <div className="relative">
      <input
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none focus:border-green-500"
      />
    </div>
  )
}
