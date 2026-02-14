import Link from "next/link";


export default function DesktopNav(){

    const links = [
        { href: "/", label: "Home" },
        { href: "/pricing", label: "Pricing" },
        { href: "/about", label: "About" },
    ];

    return (
    <nav className="hidden md:flex items-center gap-6">
        {/*5. em screens md 768px, o hidden é substituído por flex */}
      {links.map((link) => (
        // 9. Uso correto de link
        <Link
          key={link.href}
          href={link.href}
          className="text-sm font-medium text-gray-700 hover:text-blue-600 transition-colors"
        >
          {link.label}
        </Link>
      ))}
    </nav>
  );
}