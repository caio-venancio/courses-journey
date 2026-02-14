import Logo from "./components/Logo"
import DesktopNav from "./components/DesktopNav";
import MobileMenuButton from "./components/MobileMenuButton";
import '../globals.css'

export default function Header(){
    return(
        <header className="sticky top-0 z-50 bg-white/80 backdrop-blur border-b"> 
            {/*1. uso de tag semântica*/}
            {/*2. uso de stick z-50 para sticky correto */}
            <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
                {/*3. cria container com largura máxima e centralizado, com padding nas laterais e ajuste em telas*/}
                <div className="flex justify-between h-16 items-center md:justify-start md:gap-6"> 
                    {/*4. cria barra horizontal */}
                    <Logo />
                    <DesktopNav />
                    <MobileMenuButton />
                    {/*6. separação em componentes */}
                </div>
            </div>
        </header>
    )
}